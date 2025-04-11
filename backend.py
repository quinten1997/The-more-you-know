
import streamlit as st
import streamlit.components.v1 as components
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

    # Handle geolocation data
    if "auto_lat" not in st.session_state:
        st.session_state.auto_lat = None
    if "auto_lon" not in st.session_state:
        st.session_state.auto_lon = None
    st.experimental_get_query_params()  # Forces re-render to allow JS communication

    # Sidebar inputs with fallback to detected location
    st.sidebar.header("Search Options")
    use_manual = st.sidebar.checkbox("📍 Enter location manually", value=False)

    if use_manual or st.session_state.auto_lat is None:
        lat = st.sidebar.number_input("Latitude", value=52.3702, format="%f")
        lon = st.sidebar.number_input("Longitude", value=4.8952, format="%f")
    else:
        lat = st.session_state.auto_lat
        lon = st.session_state.auto_lon
        st.sidebar.success(f"Using detected location: {lat:.4f}, {lon:.4f}")

    radius_m = st.sidebar.slider("Search radius (meters)", 100, 20000, 1000, 100)
    categories = st.sidebar.multiselect("Interests/Categories", ["history", "food", "architecture", "nature"], default=["history"])
    run_search = st.sidebar.button("Find Places")

    if run_search:
        results_all = []
        results_all.append(get_opentripmap_places(lat, lon, radius_m, categories))
        if "history" in categories or "architecture" in categories:
            results_all.append(get_wikipedia_nearby(lat, lon, radius_m))
        if "food" in categories:
            results_all.append(get_osm_overpass(lat, lon, radius_m, ["amenity=restaurant", "amenity=cafe", "amenity=bar"]))
        if "nature" in categories:
            results_all.append(get_osm_overpass(lat, lon, radius_m, ["natural=peak", "leisure=park"]))

        combined = merge_results(*results_all)
        st.session_state.search_results = combined
        st.session_state.lat = lat
        st.session_state.lon = lon

    if "search_results" in st.session_state and st.session_state.search_results:
        st.subheader(f"Found {len(st.session_state.search_results)} places")
        display_map(
            st.session_state.get("lat", lat),
            st.session_state.get("lon", lon),
            st.session_state.search_results
        )
