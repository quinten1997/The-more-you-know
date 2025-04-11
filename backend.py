import streamlit as st
from fetchers.opentripmap import get_opentripmap_places
from fetchers.wikipedia import get_wikipedia_nearby
from fetchers.overpass import get_osm_overpass
from utils.geo import merge_results
from ui.map_display import display_map

def run_app_logic():
    st.title("📍 Nearby Points of Interest Explorer")

    # Initialize session state keys if not already set
    if "search_results" not in st.session_state:
        st.session_state.search_results = []
    if "lat" not in st.session_state:
        st.session_state.lat = None
    if "lon" not in st.session_state:
        st.session_state.lon = None

    with st.sidebar:
        st.header("Search Options")
        lat = st.number_input("Latitude", value=52.370216, format="%f")
        lon = st.number_input("Longitude", value=4.895168, format="%f")
        radius_m = st.slider("Search radius (meters)", 100, 20000, 1000, 100)
        categories = st.multiselect("Interests/Categories", ["history", "food", "architecture", "nature"], default=["history"])
        run_search = st.button("Find Places")

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
        run_search == False

    # Display results if they exist
    if st.session_state.search_results:
        st.subheader(f"Found {len(st.session_state.search_results)} places")
        display_map(
            st.session_state.lat or lat,
            st.session_state.lon or lon,
            st.session_state.search_results
        )
