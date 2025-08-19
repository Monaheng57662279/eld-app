from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json, math
from datetime import datetime, timezone
from .utils import geocode, route, interpolate_points_by_distance
from .hos import plan_hos

@csrf_exempt
def health(request):
    return JsonResponse({"ok": True})

@csrf_exempt
def plan_trip(request):
    if request.method != "POST":
        return JsonResponse({"error":"POST required"}, status=405)
    try:
        body = json.loads(request.body.decode("utf-8"))
        cur_q = body.get("currentLocation")
        pickup_q = body.get("pickup")
        dropoff_q = body.get("dropoff")
        cycle_used = float(body.get("currentCycleUsedHours", 0))
        # optional start time (ISO); default now UTC
        start_time = body.get("startTimeIso") or datetime.now(timezone.utc).isoformat().replace("+00:00","Z")

        if not (cur_q and pickup_q and dropoff_q):
            return JsonResponse({"error":"Missing required fields"}, status=400)

        cur = geocode(cur_q)
        pickup = geocode(pickup_q)
        dropoff = geocode(dropoff_q)

        # Route: current -> pickup -> dropoff
        r1 = route(cur, pickup)
        r2 = route(pickup, dropoff)

        total_distance_m = r1["distance_m"] + r2["distance_m"]
        total_duration_s = r1["duration_s"] + r2["duration_s"]
        total_miles = total_distance_m / 1609.34
        total_hours = total_duration_s / 3600.0

        # HOS schedule
        schedule = plan_hos(total_miles, total_hours, start_time, cycle_used)

        # Build targets for markers: breaks, fuel, off-duty starts, etc. using approx km locations
        # Collect driving segment durations to place points along path proportionally
        # Create unified path
        path = r1["path"] + r2["path"]
        total_km = total_distance_m / 1000.0

        # Heuristic: place points at cumulative km where each DRIVING segment ends
        # proportionally to distance vs time (assume constant avg speed)
        avg_speed_kmh = total_km / (total_hours or 1e-6)
        targets_km = []
        km_so_far = 0.0
        drive_hours_seen = 0.0
        miles_since_last = 0.0

        # derive targets from schedule
        for seg in schedule:
            if seg["label"] in ("Driving",):
                # driving seg length in hours
                t0 = datetime.fromisoformat(seg["start"].replace("Z","+00:00"))
                t1 = datetime.fromisoformat(seg["end"].replace("Z","+00:00"))
                hrs = (t1 - t0).total_seconds()/3600.0
                km = hrs * avg_speed_kmh
                km_so_far += km
                targets_km.append(km_so_far)

        points = interpolate_points_by_distance(path, targets_km)

        # attach coordinates back to driving segment ends
        p_i = 0
        for seg in schedule:
            if seg["label"] == "Driving" and p_i < len(points):
                seg["lat"] = points[p_i]["lat"]
                seg["lon"] = points[p_i]["lon"]
                p_i += 1

        return JsonResponse({
            "ok": True,
            "locations": {"current": cur, "pickup": pickup, "dropoff": dropoff},
            "route": {
                "distance_m": total_distance_m,
                "duration_s": total_duration_s,
                "path": path
            },
            "schedule": schedule
        })
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
