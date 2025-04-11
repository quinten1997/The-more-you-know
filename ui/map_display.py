import streamlit as st
import folium
from streamlit_folium import st_folium

def display_map(user_lat, user_lon, places):
    if not places:
        st.info("No places found in this area.")
        return None

    # Create the map and center on user location
    m = folium.Map(location=[user_lat, user_lon], zoom_start=15)
    folium.Marker(
        [user_lat, user_lon],
        popup="You are here",
        icon=folium.Icon(color="blue")
    ).add_to(m)

    # Add POI markers
    for place in places:
        lat = place.get("lat")
        lon = place.get("lon")
        if lat and lon:
            popup = f"<b>{place['name']}</b><br>{place['description']}<br>"
            if place.get('url'):
                popup += f"<a href='{place['url']}' target='_blank'>More info</a>"
            folium.Marker([lat, lon], popup=popup).add_to(m)

    # Display the map
    st.subheader("🗺️ Nearby Map")
    output = st_folium(m, width=700, height=500, returned_objects=["last_clicked"])

    # Display POI cards
    st.subheader("📌 Places Found")
    for place in places:
        st.markdown(f"### {place['name']}")
        st.write(f"**Category:** {place['category'] or 'Unknown'}")
        st.write(f"**Distance:** {place.get('distance_m', '?')} meters")
        st.write(place['description'])
        if place.get("image"):
            st.image(place["image"], width=250)
        if place.get("url"):
            st.markdown(f"[More Info]({place['url']})", unsafe_allow_html=True)
        st.markdown("---")

    # Return map click result if user clicked
    if output and output.get("last_clicked"):
        return output["last_clicked"]

    return None
