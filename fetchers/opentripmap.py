import os
import requests
from utils.summarizer import summarize_text
from utils.geo import haversine_distance

API_KEY = os.getenv("OPENTRIPMAP_API_KEY", "")

def get_opentripmap_places(lat, lon, radius, categories):
    if not API_KEY:
        return []
    kinds = []
    if "history" in categories or "architecture" in categories:
        kinds += ["historic", "architecture", "cultural"]
    if "food" in categories:
        kinds += ["foods"]
    if "nature" in categories:
        kinds += ["natural"]
    kind_str = ",".join(set(kinds)) if kinds else "interesting_places"
    url = f"https://api.opentripmap.com/0.1/en/places/radius"
    params = {
        "lat": lat,
        "lon": lon,
        "radius": radius,
        "kinds": kind_str,
        "limit": 50,
        "apikey": API_KEY,
    }
    resp = requests.get(url, params=params)
    data = resp.json()
    results = []
    for place in data.get("features", data):
        try:
            props = place.get("properties", place)
            xid = props.get("xid")
            name = props.get("name")
            dist = props.get("dist")
            kinds = props.get("kinds", "")
            category = kinds.split(',')[0] if kinds else ""
            details = {}
            if xid:
                url_det = f"https://api.opentripmap.com/0.1/en/places/xid/{xid}"
                det_resp = requests.get(url_det, params={"apikey": API_KEY})
                details = det_resp.json()
            description = ""
            if details.get("wikipedia_extracts"):
                description = details["wikipedia_extracts"].get("text", "")
            elif details.get("info"):
                desc_list = []
                if details["info"].get("descr"):
                    desc_list.append(details["info"]["descr"])
                if details["info"].get("subject"):
                    desc_list.append(details["info"]["subject"])
                description = ". ".join(desc_list)
            description = summarize_text(description)
            image_url = details.get("preview", {}).get("source")
            coords = details.get("point", {})
            results.append({
                "name": name or details.get("name", "Unnamed"),
                "category": category,
                "distance_m": int(dist) if dist else None,
                "description": description,
                "source": "OpenTripMap",
                "url": details.get("otm") or details.get("url"),
                "image": image_url,
                "lat": coords.get("lat"),
                "lon": coords.get("lon")
            })
        except:
            continue
    return results