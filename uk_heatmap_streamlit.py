import streamlit as st
import pandas as pd
import folium
from folium.plugins import HeatMap
from streamlit_folium import folium_static
import os

# Load and aggregate data
geocoded_file_path = 'geocoded_zip_codes.csv'
if os.path.exists(geocoded_file_path):
    df = pd.read_csv(geocoded_file_path)
    aggregated_data = df.groupby(['Zip Code', 'Status', 'Latitude', 'Longitude']).size().reset_index(name='Count')
else:
    aggregated_data = pd.DataFrame({
        'Zip Code': ['XYZ', 'ABC'],
        'Status': ['No Show', 'Completed'],
        'Count': [10, 15],
        'Latitude': [51.5, 53.4],
        'Longitude': [-0.1, -2.3]
    })

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