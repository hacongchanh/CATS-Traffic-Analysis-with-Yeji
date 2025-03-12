import pandas as pd
import matplotlib.pyplot as plt
import folium

# Define a consistent color map for months
month_colors = {
    'January': '#FF93C9', 'February': '#FF3B33', 'March': '#F6700C', 'April': '#F6D40C', 
    'May': '#8DF379', 'June': '#1C720C', 'July': '#43CBF5', 'August': '#186CEB', 
    'September': '#082756', 'October': '#C19CF6', 'November': '#55239F', 'December': '#000000'
}

# Load the Excel data
file_path = "C:/Users/yejijeon/OneDrive/PAG project/Enhance Traffic Count/results/weekday average/monthly_weekday_average_filtered_location.csv"
df = pd.read_csv(file_path)

# Prompt for a LOCAL_ID
print("Available LOCAL_IDs:", df['LOCAL_ID'].unique())
selected_local_id = input("Please enter a LOCAL_ID from the above list: ")

# Filter the data for the selected LOCAL_ID
df_selected = df[df['LOCAL_ID'] == selected_local_id]

if df_selected.empty:
    print(f"No data available for the selected LOCAL_ID: {selected_local_id}")
else:
    # Plotting traffic counts
    plt.figure(figsize=(12, 8))
    weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    months_ordered = ['January', 'February', 'March', 'April', 'May', 'June',
                      'July', 'August', 'September', 'October', 'November', 'December']

    for month in months_ordered:
        if month in df_selected['Month'].values:
            df_month = df_selected[df_selected['Month'] == month]
            totals = [df_month[day].values[0] for day in weekdays if day in df_month.columns]
            plt.plot(weekdays, totals, marker='o', label=month, color=month_colors[month])

    plt.title(f"Weekday Traffic Counts for {selected_local_id} Across Different Months")
    plt.xlabel("Weekday", fontsize=15)
    plt.ylabel("Traffic Count", fontsize=15)
    plt.xticks(fontsize=13)
    plt.yticks(fontsize=13)
    plt.legend(title="Month", loc='lower right')
    plt.grid(True)
    plt.show()

    # Get the latitude and longitude for the location
    latitude = df_selected['LATITUDE_FROM'].values[0]
    longitude = df_selected['LONGITUDE_FROM'].values[0]

    # Create a map centered around the location
    map_location = folium.Map(location=[latitude, longitude], zoom_start=13)
    
    # Add a marker for the intersection
    folium.Marker([latitude, longitude], tooltip='Intersection Location', popup=f'{selected_local_id}').add_to(map_location)

    # Display the map
    print(f"Displaying map for {selected_local_id} located at ({latitude}, {longitude})")
    map_location.save(f"C:/Users/yejijeon/Desktop/PAG project/Enhance Traffic Count/results/weekday average/{selected_local_id}_location.html")
    map_location