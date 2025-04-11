from math import radians, cos, sin, asin, sqrt

def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371000.0
    phi1, phi2 = radians(lat1), radians(lat2)
    dphi = radians(lat2 - lat1)
    dlambda = radians(lon2 - lon1)
    a = sin(dphi/2)**2 + cos(phi1) * cos(phi2) * sin(dlambda/2)**2
    c = 2 * asin(min(1, sqrt(a)))
    return R * c

def merge_results(*results_lists):
    merged = []
    seen_names = set()
    for lst in results_lists:
        for place in lst:
            name = place['name'].lower()
            if name in seen_names:
                continue
            seen_names.add(name)
            merged.append(place)
    merged.sort(key=lambda x: x['distance_m'] if x.get('distance_m') is not None else float('inf'))
    return merged