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

# Calculate the duration of D2 drought for each week
alabama_data['Duration'] = (alabama_data['ValidEnd'] - alabama_data['ValidStart']).dt.days

# Group by FIPS and count the number of weeks in D2
count_d2_weeks = alabama_data[alabama_data['D2'] > 0].groupby('FIPS')['FIPS'].count().reset_index(name='WeeksInD2')

# Filter counties with D2 drought for 8 or more weeks
count_d2_weeks = count_d2_weeks[count_d2_weeks['WeeksInD2'] >= 8]

# Merge with the original data to get the geometry
final_data = gdf.merge(count_d2_weeks, on='FIPS')

# Plot the map
fig, ax = plt.subplots(1, 1, figsize=(10, 10))
ax.set_title('Alabama Counties in D2 Drought for 8 or More Weeks')

# Plot Alabama counties
alabama_data.boundary.plot(ax=ax, color='black', linewidth=1)
alabama_data.plot(ax=ax, color='lightgray', edgecolor='black')

# Plot counties in D2 drought for 8 or more weeks
final_data.plot(ax=ax, color='red', edgecolor='black', aspect='equal')

# Display all Alabama county names as annotations
for x, y, label in zip(alabama_data.geometry.centroid.x, alabama_data.geometry.centroid.y, alabama_data['NAME']):
    ax.text(x, y, label, fontsize=8, ha='center', va='center', color='black')

plt.show()
