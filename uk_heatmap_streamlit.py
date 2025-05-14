import streamlit as st
import pandas as pd
import folium
from folium.plugins import HeatMap
from streamlit_folium import folium_static
import os

# Load and aggregate data
geocoded_file_path = 'dentist_data_map.csv'
df = pd.read_csv(geocoded_file_path)
receiving_cases = df.groupby(['postcode', 'latitude', 'longitude'])['receiving_cases'] * 30 
availability = df['weekly_availability_hours'] * 60 
ratio = availability / receiving_cases


# Streamlit app title
st.title("UK Postal Code Density Map with Status Filter")

# Dropdown for status filter
status = st.selectbox("Select Status", options=['All'] + list(aggregated_data['Status'].unique()), index=0)

# Filter data based on status
filtered_data = aggregated_data if status == 'All' else aggregated_data[aggregated_data['Status'] == status]

# Create Folium map with heatmap
m = folium.Map(location=[55.3781, -3.4360], zoom_start=6)
heat_data = [[row['Latitude'], row['Longitude'], row['Count']] for _, row in filtered_data.iterrows()]
HeatMap(heat_data, radius=15, max_zoom=13).add_to(m)

# Display the map
folium_static(m)