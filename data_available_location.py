import pandas as pd
import folium

# Paths for the data files
count_file_path = "C:/Users/yejijeon/Downloads/ProcessedPAGData/PAGData/PAG_Count_1995-2023.csv"
location_file_path = "C:/Users/yejijeon/OneDrive/PAG project/Enhance Traffic Count/data/ProcessedPAGData/PAG_locations_2023.csv"

# Load the count data
df = pd.read_csv(count_file_path)

# Load the location data
locations_df = pd.read_csv(location_file_path)

# Convert 'ST_DATE' to datetime
df['ST_DATE'] = pd.to_datetime(df['ST_DATE'])

# Merge count data with location data on 'LOCAL_ID'
df = pd.merge(df, locations_df[['LOCAL_ID', 'LATITUDE_FROM', 'LONGITUDE_FROM']], on='LOCAL_ID', how='left')

# Filter data for the years 2018-2022
df = df[(df['ST_DATE'].dt.year >= 2018) & (df['ST_DATE'].dt.year <= 2022)]

def create_location_map(unique_locations, year):
    # Initialize a Folium map with the "Carto Positron" background
    map = folium.Map(location=[33.4484, -112.0740], zoom_start=10, tiles='CartoDB Positron')

    # Add circle markers for all non-NaN locations
    for _, row in unique_locations.iterrows():
        # Determine color based on whether the LOCAL_ID is a Miovision data point
        color = 'yellow' if row['LOCAL_ID'].startswith('M') else 'blue'
        
        folium.CircleMarker(
            location=[row['LATITUDE_FROM'], row['LONGITUDE_FROM']],
            radius=5,  # Specifies the radius of the circle marker
            color=color,  # Color of the circle marker's border based on the data source
            fill=True,  # Set fill to True to make the circle filled
            fillColor=color,  # Color to fill the circle
            fillOpacity=0.7  # Opacity of the fill
        ).add_to(map)
    
    map.save(f"C:/Users/yejijeon/OneDrive/PAG project/Enhance Traffic Count/results/map_{year}.html")

# Prepare a DataFrame to store available dates results
available_dates_results = []

for year in range(2018, 2023):
    year_data = df[df['ST_DATE'].dt.year == year]
    # Correct the filtering logic within the lambda function
    major_locations = year_data[year_data['LOCAL_ID'].apply(
        lambda x: not any(suffix in x for suffix in ["_EB", "_WB", "_NB", "_SB"]) and not x.startswith('M')
    )]
    unique_major_locations = major_locations[['LOCAL_ID', 'LATITUDE_FROM', 'LONGITUDE_FROM']].drop_duplicates().dropna(subset=['LATITUDE_FROM', 'LONGITUDE_FROM'])
    if not unique_major_locations.empty:
        create_location_map(unique_major_locations, year)
        # Count unique major locations for each year
        major_location_count = len(unique_major_locations)
        print(f"Map for {year} saved. Total major locations available: {major_location_count}")


# Convert the results list to a DataFrame
available_dates_df = pd.DataFrame(available_dates_results)

# Save the results to a CSV file
output_path = "C:/Users/yejijeon/OneDrive/PAG project/Enhance Traffic Count/results/available_dates_analysis.csv"
available_dates_df.to_csv(output_path, index=False)
print(f"Available dates analysis saved to {output_path}")