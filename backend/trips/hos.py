from datetime import datetime, timedelta, timezone

# Constants based on FMCSA for property-carrying drivers
MAX_DRIVE_HRS_PER_DAY = 11
MAX_ON_DUTY_WINDOW = 14
BREAK_AFTER_DRIVE_HRS = 8
BREAK_DURATION_HRS = 0.5  # 30 minutes
OFF_DUTY_BETWEEN_SHIFTS = 10  # hours
FUEL_EVERY_MILES = 1000
FUEL_DURATION_HRS = 0.5
PICKUP_DROPOFF_HRS = 1.0

def hours_to_td(h): return timedelta(hours=h)

def plan_hos(total_miles, total_drive_hours, start_dt_iso, cycle_used_hours=0):
    """
    Produce a multi-day duty schedule given total miles/duration.
    We treat fueling every 1000 miles as 30min on-duty, pickup & dropoff 1hr.
    Returns list of segments across days: each is dict with start, end, status.
    Status: OFF_DUTY, ON_DUTY, DRIVING
    """
    start = datetime.fromisoformat(start_dt_iso.replace("Z","+00:00")).astimezone(timezone.utc)
    segments = []

    remaining_drive_hours = total_drive_hours
    remaining_miles = total_miles

    # Add pickup at t0: 1 hour on-duty not driving
    cur = start
    pickup_end = cur + hours_to_td(PICKUP_DROPOFF_HRS)
    segments.append(seg(cur, pickup_end, "ON_DUTY", "Pickup"))
    cur = pickup_end

    # Track cycle: 70 hours in 8 days. We only track used so far (input) and add on-duty.
    cycle_used = cycle_used_hours

    miles_since_fuel = 0.0

    day_index = 0
    while remaining_drive_hours > 0.01 or remaining_miles > 1:
        # Start of on-duty window
        on_duty_start = cur
        on_duty_used = 0.0
        drove_this_shift = 0.0
        drive_left_today = min(MAX_DRIVE_HRS_PER_DAY, remaining_drive_hours)
        window_left = MAX_ON_DUTY_WINDOW

        # Keep cycling within on-duty window
        while drive_left_today > 0.01 and window_left > 0.01:
            # Need a 30-min break before exceeding 8 hours driving since last break/off-duty
            need_break = drove_this_shift >= BREAK_AFTER_DRIVE_HRS - 1e-6
            if need_break and window_left >= BREAK_DURATION_HRS:
                brk = hours_to_td(BREAK_DURATION_HRS)
                segments.append(seg(cur, cur + brk, "OFF_DUTY", "30-min break"))
                cur += brk
                window_left -= BREAK_DURATION_HRS
                cycle_used += BREAK_DURATION_HRS
                drove_this_shift = 0.0  # after break counter resets for the 8-hr rule

            # Determine next driving chunk: up to remaining drive today, up to remaining in 8-hr before break,
            # and up to window_left.
            chunk = min(drive_left_today, 8 - drove_this_shift, window_left, remaining_drive_hours)
            if chunk <= 0.01:
                break

            # Also ensure we don't go past the next fuel requirement
            # Estimate miles per hour from overall pace
            pace_mph = total_miles / total_drive_hours if total_drive_hours > 0 else 50.0
            miles_chunk = pace_mph * chunk

            if miles_since_fuel + miles_chunk > FUEL_EVERY_MILES and remaining_miles > 0:
                # Split chunk to fuel before exceeding limit
                miles_to_fuel = FUEL_EVERY_MILES - miles_since_fuel
                hrs_to_fuel = miles_to_fuel / pace_mph if pace_mph > 0 else chunk
                hrs_to_fuel = max(0.01, min(chunk, hrs_to_fuel))
                # Drive to fuel
                segments.append(seg(cur, cur + hours_to_td(hrs_to_fuel), "DRIVING", "Driving"))
                cur += hours_to_td(hrs_to_fuel)
                drive_left_today -= hrs_to_fuel
                remaining_drive_hours -= hrs_to_fuel
                remaining_miles -= pace_mph * hrs_to_fuel
                window_left -= hrs_to_fuel
                cycle_used += hrs_to_fuel
                drove_this_shift += hrs_to_fuel
                miles_since_fuel += pace_mph * hrs_to_fuel

                # Fuel stop
                if window_left >= FUEL_DURATION_HRS:
                    segments.append(seg(cur, cur + hours_to_td(FUEL_DURATION_HRS), "ON_DUTY", "Fueling"))
                    cur += hours_to_td(FUEL_DURATION_HRS)
                    window_left -= FUEL_DURATION_HRS
                    cycle_used += FUEL_DURATION_HRS
                    miles_since_fuel = 0.0
                else:
                    # No time to fuel in window -> end shift
                    break
            else:
                # Normal drive
                segments.append(seg(cur, cur + hours_to_td(chunk), "DRIVING", "Driving"))
                cur += hours_to_td(chunk)
                drive_left_today -= chunk
                remaining_drive_hours -= chunk
                remaining_miles -= miles_chunk
                window_left -= chunk
                cycle_used += chunk
                drove_this_shift += chunk
                miles_since_fuel += miles_chunk

        # End of shift; take 10 hours off-duty if still remaining work
        if remaining_drive_hours > 0.01 or remaining_miles > 1:
            off = hours_to_td(OFF_DUTY_BETWEEN_SHIFTS)
            segments.append(seg(cur, cur + off, "OFF_DUTY", "Off-duty"))
            cur += off
            day_index += 1

    # Arrive / drop-off
    segments.append(seg(cur, cur + hours_to_td(PICKUP_DROPOFF_HRS), "ON_DUTY", "Drop-off"))
    return segments

def seg(start_dt, end_dt, status, label):
    return {
        "start": start_dt.isoformat().replace("+00:00","Z"),
        "end": end_dt.isoformat().replace("+00:00","Z"),
        "status": status,
        "label": label
    }
