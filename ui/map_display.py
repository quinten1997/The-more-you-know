import streamlit as st
import folium
from streamlit_folium import st_folium

def display_map(user_lat, user_lon, places):
    if not places:
        st.info("No places found in this area.")
        return None

    m = folium.Map(location=[user_lat, user_lon], zoom_start=15)

    folium.Marker(
        [user_lat, user_lon],
        popup="You are here",
        icon=folium.Icon(color="blue", icon="user")
    ).add_to(m)

    for place in places:
        lat = place.get("lat")
        lon = place.get("lon")
        if lat and lon:
            html = f"""
                <h4>{place['name']}</h4>
                <p>{place['description']}</p>
            """
            if place.get('image'):
                html += f"<img src='{place['image']}' width='200'><br>"
            if place.get('url'):
                html += f"<a href='{place['url']}' target='_blank'>More info</a>"

            iframe = folium.IFrame(html=html, width=250, height=300)
            popup = folium.Popup(iframe, max_width=250)
            tooltip = place['name']

            folium.Marker(
                [lat, lon],
                popup=popup,
                tooltip=tooltip,
                icon=folium.Icon(color="green", icon="info-sign")
            ).add_to(m)

    st.subheader("🗺️ Nearby Map")
    output = st_folium(m, width=700, height=500, returned_objects=["last_clicked"])

    st.subheader("📌 Places Found")
    for place in places:
        st.markdown(f"### {place['name']}")
        st.write(f"**Category:** {place.get('category', 'Unknown')}")
        st.write(f"**Distance:** {place.get('distance_m', '?')} meters")
        st.write(place['description'])
        if place.get("image"):
            st.image(place["image"], width=250)
        if place.get("url"):
            st.markdown(f"[More Info]({place['url']})", unsafe_allow_html=True)
        st.markdown("---")

    if output and output.get("last_clicked"):
        return output["last_clicked"]

    return None
