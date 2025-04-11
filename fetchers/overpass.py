import requests
from utils.geo import haversine_distance

def get_osm_overpass(lat, lon, radius, tags):
    url = "https://overpass-api.de/api/interpreter"
    criteria = ""
    if tags:
        criteria += "("
        for t in tags:
            if "=" in t:
                k, v = t.split("=", 1)
                criteria += f"node(around:{radius},{lat},{lon})[{k}={v}];"
            else:
                criteria += f"node(around:{radius},{lat},{lon})[{t}];"
        criteria += ");"
    query = f"[out:json];{criteria}out center;"
    try:
        resp = requests.get(url, params={'data': query}, timeout=10)
        data = resp.json()
    except:
        return []
    results = []
    for el in data.get("elements", []):
        if el.get("tags") and el.get("lat") and el.get("lon"):
            name = el["tags"].get("name", "Unnamed")
            cat = next((el["tags"].get(k) for k in ["amenity", "tourism", "historic", "shop"] if el["tags"].get(k)), "")
            dist = haversine_distance(lat, lon, el["lat"], el["lon"])
            results.append({
                "name": name,
                "category": cat,
                "distance_m": int(dist),
                "description": "",
                "source": "OSM",
                "url": f"https://www.openstreetmap.org/node/{el.get('id')}",
                "image": None,
                "lat": el.get("lat"),
                "lon": el.get("lon")
            })
    return results