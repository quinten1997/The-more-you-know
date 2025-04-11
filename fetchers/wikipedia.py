import requests
from utils.summarizer import summarize_text
from utils.geo import haversine_distance

def get_wikipedia_nearby(lat, lon, radius, max_results=1):
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "generator": "geosearch",
        "ggscoord": f"{lat}|{lon}",
        "ggsradius": radius,
        "ggslimit": max_results,
        "prop": "coordinates|pageimages|description|extracts",
        "explaintext": True,
        "exintro": True,
        "pithumbsize": 200,
        "format": "json"
    }
    try:
        resp = requests.get(url, params=params)
        data = resp.json()
    except:
        return []
    pages = data.get("query", {}).get("pages", {})
    results = []
    for page_id, page in pages.items():
        title = page.get("title")
        desc = page.get("description", "")
        extract = page.get("extract", "")
        summary = extract.strip() if extract else desc
        summary = summarize_text(summary)
        thumb = page.get("thumbnail", {}).get("source")
        coords = page.get("coordinates", [{}])[0]
        lat2 = coords.get("lat")
        lon2 = coords.get("lon")
        dist = haversine_distance(lat, lon, lat2, lon2) if lat2 and lon2 else None
        results.append({
            "name": title,
            "category": desc,
            "distance_m": int(dist) if dist else None,
            "description": summary,  # ✅ summarized!
            "source": "Wikipedia",
            "url": f"https://en.wikipedia.org/wiki/{title.replace(' ', '_')}",
            "image": thumb,
            "lat": lat2,
            "lon": lon2
        })
    return results