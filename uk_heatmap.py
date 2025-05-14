import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import folium
from folium.plugins import HeatMap
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

# Initialize Dash app
app = dash.Dash(__name__)

# Create base heatmap if it does not exist
if not os.path.exists("base_map.html"):
    m = folium.Map(location=[55.3781, -3.4360], zoom_start=6)
    
    # Heatmap data, using (latitude, longitude, weight)
    heat_data = [[row['Latitude'], row['Longitude'], row['Count']] for _, row in aggregated_data.iterrows()]
    HeatMap(heat_data, radius=15, max_zoom=13).add_to(m)
    
    m.save("base_map.html")

# Read base map HTML for initial display
with open("base_map.html", "r") as f:
    map_html = f.read()

# Dash app layout
app.layout = html.Div([
    html.H1("UK Postal Code Density Map with Status Filter"),
    
    # Dropdown for filtering by status
    dcc.Dropdown(
        id='status-filter',
        options=[{'label': status, 'value': status} for status in aggregated_data['Status'].unique()] + [{'label': 'All', 'value': 'All'}],
        value='All',
        clearable=False,
    ),
    
    # Div to embed the Folium map
    html.Iframe(id='map', srcDoc=map_html, width='100%', height='600')
])

# Callback to update heatmap based on selected status
@app.callback(
    Output('map', 'srcDoc'),
    Input('status-filter', 'value')
)
def update_map(selected_status):
    # Filter data based on selected status
    filtered_data = aggregated_data if selected_status == 'All' else aggregated_data[aggregated_data['Status'] == selected_status]
    
    # Generate a new Folium map with heatmap based on the filtered data
    m = folium.Map(location=[55.3781, -3.4360], zoom_start=6)
    
    # Prepare heatmap data
    heat_data = [[row['Latitude'], row['Longitude'], row['Count']] for _, row in filtered_data.iterrows()]
    
    # Add the heatmap layer
    HeatMap(heat_data, radius=15, max_zoom=13).add_to(m)
    
    # Save the updated map and return as iframe
    m.save("filtered_map.html")
    with open("filtered_map.html", "r") as f:
        return f.read()

# Run the Dash app
app.run(debug=True)