import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Load shapefile
shapefile_path = 'UScounties\\UScounties.shp'
gdf = gpd.read_file(shapefile_path)

# Load CSV data
csv_path = 'USDM_AL.csv'
csv_data = pd.read_csv(csv_path, dtype={'FIPS': str})

# Merge the shapefile and CSV data based on the FIPS column
merged_data = gdf.merge(csv_data, on='FIPS')

# Filter data for Alabama
alabama_data = merged_data[merged_data['State'] == 'AL']

# Convert 'ValidStart' and 'ValidEnd' to datetime format
alabama_data['ValidStart'] = pd.to_datetime(alabama_data['ValidStart'])
alabama_data['ValidEnd'] = pd.to_datetime(alabama_data['ValidEnd'])

# Check if any week is in D3 drought
alabama_data['InD3'] = (alabama_data['D3'] > 0).astype(int)

# Group by FIPS and sum the 'InD3' column
count_d3_weeks = alabama_data.groupby('FIPS')['InD3'].sum().reset_index(name='WeeksInD3')

# Filter counties with D3 drought for at least one week
count_d3_weeks = count_d3_weeks[count_d3_weeks['WeeksInD3'] > 0]

# Merge with the original data to get the geometry
final_data = gdf.merge(count_d3_weeks, on='FIPS')

# Plot the map
fig, ax = plt.subplots(1, 1, figsize=(10, 10))
ax.set_title('Alabama Counties in D3 Drought at Any Time')

# Plot Alabama counties
alabama_data.boundary.plot(ax=ax, color='black', linewidth=1)
alabama_data.plot(ax=ax, color='lightgray', edgecolor='black')

# Plot counties in D3 drought for at least one week
final_data.plot(ax=ax, color='red', edgecolor='black', aspect='equal')

# Display all Alabama county names as annotations
for x, y, label in zip(alabama_data.geometry.centroid.x, alabama_data.geometry.centroid.y, alabama_data['NAME']):
    ax.text(x, y, label, fontsize=8, ha='center', va='center', color='black')

plt.show()
