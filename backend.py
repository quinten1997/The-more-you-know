import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime, timedelta
from fetchers.opentripmap import get_opentripmap_places
from fetchers.wikipedia import get_wikipedia_nearby
from fetchers.overpass import get_osm_overpass
from utils.geo import merge_results
from ui.map_display import display_map

def run_app_logic():
    st.title("📍 Nearby Points of Interest Explorer")

    # Inject JavaScript to get user's geolocation
    components.html(
        """
        <script>
        navigator.geolocation.getCurrentPosition(
            (position) => {
                const lat = position.coords.latitude;
                const lon = position.coords.longitude;
                const data = {latitude: lat, longitude: lon};
                window.parent.postMessage({type: 'set-location', data: data}, '*');
            }
        );
        </script>
        """,
        height=0,
    )
    # Hidden input to receive coordinates from JavaScript
    user_loc = st.text_input("Detected location", key="user_geo")

    # Parse and store in session
    if user_loc and "," in user_loc:
        try:
            auto_lat, auto_lng = map(float, user_loc.split(","))
            st.session_state.auto_lat = auto_lat
            st.session_state.auto_lng = auto_lng
        except ValueError:
            st.warning("Could not parse auto-detected location.")

    # Init session vars
    for key in ["auto_lat", "auto_lng", "lat", "lng", "search_results", "last_check", "custom_point"]:
        if key not in st.session_state:
            st.session_state[key] = None if key != "search_results" else []

    st.sidebar.header("Search Options")
    use_manual = st.sidebar.checkbox("📍 Enter location manually", value=False)
    use_custom_point = st.sidebar.checkbox("🗺️ Use point clicked on map", value=False)

    if use_manual:
        lat = st.sidebar.number_input("Latitude", value=52.3702, format="%f")
        lng = st.sidebar.number_input("Longitude", value=4.8952, format="%f")
    elif use_custom_point and st.session_state.get("custom_point"):
        lat, lng = st.session_state["custom_point"]
        st.sidebar.success(f"Using map click: {lat:.4f}, {lng:.4f}")
    elif st.session_state.auto_lat is not None:
        lat = st.session_state.auto_lat
        lng = st.session_state.auto_lng
        st.sidebar.success(f"Using detected location: {lat:.4f}, {lng:.4f}")
    else:
        st.info("Waiting for location... Using fallback (Amsterdam).")
        lat, lng = 52.3702, 4.8952

    st.session_state.lat = lat
    st.session_state.lng = lng

    radius_m = st.sidebar.slider("Search radius (meters)", 100, 20000, 1000, 100)
    categories = st.sidebar.multiselect("Interests/Categories", ["history", "food", "architecture", "nature"], default=["history"])
    num_pois = st.sidebar.slider("Max POIs per source", min_value=1, max_value=25, value=1)
    interval_minutes = st.sidebar.number_input("Update interval (minutes)", min_value=1, max_value=1440, value=10)
    refresh_now = st.sidebar.button("🔄 Refresh POIs Now")

    # Refresh logic
    now = datetime.utcnow()
    time_to_refresh = (
        st.session_state.last_check is None or
        now - st.session_state.last_check > timedelta(minutes=interval_minutes)
    )

    if refresh_now or time_to_refresh:
        results_all = []

        # Limit each fetch to 1 item to reduce load
        otm = get_opentripmap_places(lat, lng, radius_m, categories)
        if otm: results_all.append(otm[:1])

        if "history" in categories or "architecture" in categories:
            wiki = get_wikipedia_nearby(lat, lng, radius_m, max_results=num_pois)
            if wiki: results_all.append(wiki[:num_pois])

        if "food" in categories:
            osm_food = get_osm_overpass(lat, lng, radius_m, ["amenity=restaurant", "amenity=cafe", "amenity=bar"])
            if osm_food: results_all.append(osm_food[:num_pois])

        if "nature" in categories:
            osm_nature = get_osm_overpass(lat, lng, radius_m, ["natural=peak", "leisure=park"])
            if osm_nature: results_all.append(osm_nature[:num_pois])

        combined = merge_results(*results_all)
        st.session_state.search_results = combined
        st.session_state.last_check = now

    if st.session_state.search_results:
        st.subheader(f"Found {len(st.session_state.search_results)} places")
        clicked_point = display_map(lat, lng, st.session_state.search_results)

        if clicked_point:
            st.session_state["custom_point"] = (clicked_point["lat"], clicked_point["lng"])
