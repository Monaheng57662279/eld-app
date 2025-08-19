import math, requests, time

OSRM_ROUTE = "https://router.project-osrm.org/route/v1/driving/{lon1},{lat1};{lon2},{lat2}?overview=full&geometries=geojson"
NOMINATIM_SEARCH = "https://nominatim.openstreetmap.org/search"

def geocode(query):
    params = {"q": query, "format":"json", "limit":1}
    headers = {"User-Agent": "ELD-Planner-Demo/1.0"}
    r = requests.get(NOMINATIM_SEARCH, params=params, headers=headers, timeout=15)
    r.raise_for_status()
    data = r.json()
    if not data: raise ValueError(f"Could not geocode: {query}")
    lat = float(data[0]["lat"]); lon=float(data[0]["lon"])
    display = data[0].get("display_name", query)
    return {"lat":lat,"lon":lon,"label":display}

def route(a, b):
    url = OSRM_ROUTE.format(
        lon1=a["lon"], lat1=a["lat"],
        lon2=b["lon"], lat2=b["lat"]
    )
    headers = {"User-Agent": "ELD-Planner-Demo/1.0"}
    r = requests.get(url, headers=headers, timeout=30)
    r.raise_for_status()
    data = r.json()
    if not data.get("routes"):
        raise ValueError("No route found")
    r0 = data["routes"][0]
    distance_m = r0["distance"]
    duration_s = r0["duration"]
    coords = r0["geometry"]["coordinates"]  # [ [lon,lat], ... ]
    # Convert to lat,lon pairs
    path = [{"lat": lat, "lon": lon} for lon,lat in coords]
    return {
        "distance_m": distance_m,
        "duration_s": duration_s,
        "path": path
    }

def haversine(a, b):
    # a,b: dict with lat,lon degrees; return kilometers
    R = 6371.0
    lat1, lon1 = math.radians(a["lat"]), math.radians(a["lon"])
    lat2, lon2 = math.radians(b["lat"]), math.radians(b["lon"])
    dlat = lat2 - lat1; dlon = lon2 - lon1
    h = math.sin(dlat/2)**2 + math.cos(lat1)*math.cos(lat2)*math.sin(dlon/2)**2
    return 2*R*math.asin(math.sqrt(h))

def interpolate_points_by_distance(path, targets_km):
    # Given a path [ {lat,lon} ], return points at cumulative distances (km) closest to targets.
    if not path: return []
    cum = [0.0]
    for i in range(1,len(path)):
        cum.append(cum[-1] + haversine(path[i-1], path[i]))
    res = []
    for t in targets_km:
        # find segment where cum crosses t
        if t <= 0: res.append(path[0]); continue
        if t >= cum[-1]: res.append(path[-1]); continue
        lo, hi = 0, len(cum)-1
        while lo < hi:
            mid = (lo+hi)//2
            if cum[mid] < t: lo = mid+1
            else: hi = mid
        idx = max(1, lo)
        # linear interpolation
        prev_d = cum[idx-1]; next_d = cum[idx]
        frac = (t - prev_d) / max(1e-9, (next_d - prev_d))
        A = path[idx-1]; B = path[idx]
        lat = A["lat"] + (B["lat"] - A["lat"]) * frac
        lon = A["lon"] + (B["lon"] - A["lon"]) * frac
        res.append({"lat":lat,"lon":lon})
    return res
