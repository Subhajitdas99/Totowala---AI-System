import sys
import os

# Fix import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from geopy.distance import geodesic

from backend.clustering import cluster_passengers
from backend.route_optimizer import optimize_route

st.set_page_config(layout="wide")

st.title("🚖 TOTOWALA")

# ---------------- STATE ----------------
if "passengers" not in st.session_state:
    st.session_state.passengers = []

if "groups" not in st.session_state:
    st.session_state.groups = []

# ---------------- SIDEBAR ----------------
st.sidebar.header("Add Passenger")

name = st.sidebar.text_input("Passenger Name")
lat = st.sidebar.number_input("Latitude", value=26.7271)
lon = st.sidebar.number_input("Longitude", value=88.3953)

if st.sidebar.button("Add Passenger"):
    if name:
        st.session_state.passengers.append({
            "name": name,
            "lat": lat,
            "lon": lon
        })
        st.success(f"{name} added successfully ✅")
    else:
        st.warning("Please enter a name")

# ---------------- PASSENGER LIST ----------------
st.write("### 📋 Passenger List")

if st.session_state.passengers:
    df = pd.DataFrame(st.session_state.passengers)
    st.dataframe(df)
else:
    st.write("No passengers added yet")

# ---------------- OPTIMIZE BUTTON ----------------
optimize = st.button("🚀 Optimize Rides")

if optimize:
    groups = cluster_passengers(st.session_state.passengers)

    optimized_groups = []
    for group in groups:
        optimized_groups.append(optimize_route(group))

    st.session_state.groups = optimized_groups

# ---------------- MAP ----------------
st.write("### 🗺️ Passenger Map & Routes")

if st.session_state.passengers:
    first = st.session_state.passengers[0]
    m = folium.Map(location=[first['lat'], first['lon']], zoom_start=12)

    colors = ["red", "green", "blue", "purple", "orange"]

    # Draw routes + numbered markers
    if st.session_state.groups:
        for i, group in enumerate(st.session_state.groups):

            color = colors[i % len(colors)]

            # Draw route line
            coords = [(p['lat'], p['lon']) for p in group]

            folium.PolyLine(
                coords,
                color=color,
                weight=5,
                opacity=0.8
            ).add_to(m)

            # Numbered stops
            for j, p in enumerate(group):
                folium.Marker(
                    [p['lat'], p['lon']],
                    popup=f"{p['name']} (Stop {j+1})",
                    icon=folium.DivIcon(
                        html=f"""
                        <div style="
                            font-size: 12px;
                            color: white;
                            background-color: {color};
                            border-radius: 50%;
                            width: 25px;
                            height: 25px;
                            text-align: center;
                            line-height: 25px;">
                            {j+1}
                        </div>
                        """
                    )
                ).add_to(m)

            # Show table
            st.write(f"### 🚗 Toto {i+1}")
            st.dataframe(pd.DataFrame(group))

            # Calculate distance
            total_distance = 0
            for k in range(len(group) - 1):
                p1 = group[k]
                p2 = group[k + 1]

                total_distance += geodesic(
                    (p1['lat'], p1['lon']),
                    (p2['lat'], p2['lon'])
                ).km

            st.write(f"📏 Total Distance: {total_distance:.2f} km")

    st_folium(m, width=1000, height=500)

else:
    st.write("No passengers to show on map")