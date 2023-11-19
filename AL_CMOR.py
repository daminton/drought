import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt

# Load shapefile
gdf = gpd.read_file('UScounties\\UScounties.shp')

# Load CSV data
csv_data = pd.read_csv('USDM_AL.csv', dtype={'FIPS': str})

# Load the AL_CMOR.csv data without a header
cmor_data = pd.read_csv('AL_CMOR.csv', header=None)

# Merge the shapefile and CSV data based on the FIPS column
merged_data = gdf.merge(csv_data, on='FIPS')

# Filter data for Alabama
alabama_data = merged_data[merged_data['State'] == 'AL']

# Filter out unwanted value from AL_CMOR.csv column
filtered_cmor_data = cmor_data[cmor_data.iloc[:, 1] != 'Select a county:']

# Count occurrences of each item in name_list in filtered_cmor_data
occurrences_count = filtered_cmor_data.iloc[:, 1].astype(str).value_counts().to_dict()

# Plot the map for Alabama only
fig, ax = plt.subplots(figsize=(12, 8))

# Plot the counties for Alabama
alabama_data.plot(ax=ax, color='lightgrey', edgecolor='black')

# Display Alabama county names as annotations with occurrences count (vertically stacked)
for x, y, label in zip(alabama_data.geometry.centroid.x, alabama_data.geometry.centroid.y, alabama_data['NAME']):
    occurrences = occurrences_count.get(label, 0)
    ax.text(x, y, f"{label}\n{occurrences}", fontsize=8, ha='center', va='center', color='black')

plt.title('Alabama Counties with Occurrences Count from AL_CMOR.csv')
plt.show()
