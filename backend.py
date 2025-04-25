import streamlit as st
from datetime import datetime, timedelta
from fetchers.opentripmap import get_opentripmap_places
from fetchers.wikipedia import get_wikipedia_nearby
from fetchers.overpass import get_osm_overpass
from utils.geo import merge_results
from ui.map_display import display_map
from streamlit_js_eval import get_geolocation
import geocoder
import requests

LOCATION_REFRESH_INTERVAL = 5  # seconds

def get_location_fallback():
    g = geocoder.ip('me')
    if g.ok:
        return g.latlng[0], g.latlng[1]

    try:
        response = requests.get('https://ipapi.co/json/')
        if response.status_code == 200:
            data = response.json()
            return data['latitude'], data['longitude']
    except:
        pass
    return 52.3702, 4.8952  # Default fallback (Amsterdam)

def run_app_logic():
    st.title("📍 Nearby Points of Interest Explorer")

    # Initialize session state
    for key in ["lat", "lng", "last_geo_update", "last_check", "search_results", "custom_point"]:
        if key not in st.session_state:
            st.session_state[key] = None if key != "search_results" else []

    # Get current UTC time
    now = datetime.utcnow()
    last_geo = st.session_state["last_geo_update"]
    geo_is_stale = last_geo is None or (now - last_geo > timedelta(seconds=LOCATION_REFRESH_INTERVAL))

    # Refresh geolocation if stale
    if geo_is_stale:
        location = get_geolocation()
        if location and location.get("coords"):
            lat = location["coords"]["latitude"]
            lng = location["coords"]["longitude"]
            st.session_state.lat = lat
            st.session_state.lng = lng
            st.session_state.last_geo_update = now
            st.sidebar.success(f"Location updated: {lat:.4f}, {lng:.4f}")
        elif st.session_state.lat is None or st.session_state.lng is None:
            # No live data and nothing stored — fallback
            lat, lng = get_location_fallback()
            st.session_state.lat = lat
            st.session_state.lng = lng
            st.sidebar.warning(f"Fallback location used: {lat:.4f}, {lng:.4f}")
    else:
        lat = st.session_state.lat
        lng = st.session_state.lng

    st.sidebar.header("Search Options")
    use_manual = st.sidebar.checkbox("📍 Enter location manually", value=False)
    use_custom_point = st.sidebar.checkbox("🗺️ Use point clicked on map", value=False)

    if use_manual:
        lat = st.sidebar.number_input("Latitude", value=lat, format="%f")
        lng = st.sidebar.number_input("Longitude", value=lng, format="%f")
    elif use_custom_point and st.session_state.get("custom_point"):
        lat, lng = st.session_state["custom_point"]
        st.sidebar.success(f"Using clicked location: {lat:.4f}, {lng:.4f}")
    else:
        st.sidebar.write(f"Tracking location: {lat:.4f}, {lng:.4f}")

    radius_m = st.sidebar.slider("Search radius (meters)", 100, 20000, 1000, 100)
    categories = st.sidebar.multiselect(
        "Interests/Categories",
        ["history", "food", "architecture", "nature"],
        default=["history"]
    )
    num_pois = st.sidebar.slider("Max POIs per source", min_value=1, max_value=25, value=1)
    interval_minutes = st.sidebar.number_input(
        "Update interval (minutes)", min_value=1, max_value=1440, value=10
    )
    refresh_now = st.sidebar.button("🔄 Refresh POIs Now")
    st.sidebar.caption(f"📡 Last location update: {st.session_state.last_geo_update.strftime('%H:%M:%S')}")


    last_check = st.session_state.get("last_check")
    should_update_pois = (
        refresh_now or
        last_check is None or
        (now - last_check > timedelta(minutes=interval_minutes))
    )

    if should_update_pois:
        results_all = []

        otm = get_opentripmap_places(lat, lng, radius_m, categories)
        if otm:
            results_all.extend(otm[:num_pois])

        if any(cat in categories for cat in ["history", "architecture"]):
            wiki = get_wikipedia_nearby(lat, lng, radius_m, max_results=num_pois)
            if wiki:
                results_all.extend(wiki[:num_pois])

        if "food" in categories:
            osm_food = get_osm_overpass(lat, lng, radius_m, ["amenity=restaurant", "amenity=cafe", "amenity=bar"])
            if osm_food:
                results_all.extend(osm_food[:num_pois])

        if "nature" in categories:
            osm_nature = get_osm_overpass(lat, lng, radius_m, ["natural=peak", "leisure=park"])
            if osm_nature:
                results_all.extend(osm_nature[:num_pois])

        combined = merge_results(results_all)
        st.session_state.search_results = combined
        st.session_state.last_check = now

    if st.session_state.get("search_results"):
        st.subheader(f"Found {len(st.session_state.search_results)} places")
        clicked_point = display_map(lat, lng, st.session_state.search_results)
        if clicked_point:
            st.session_state["custom_point"] = (clicked_point["lat"], clicked_point["lng"])
