from bs4 import BeautifulSoup
import pandas as pd
import folium
from sklearn.cluster import KMeans

pd.options.mode.chained_assignment = None  # default='warn'

# Read HTML content from file
with open('./resources/station_ids.html', 'r', encoding='utf-8') as file:
    html = file.read()

# Parse HTML
soup = BeautifulSoup(html, 'html.parser')

# Find the table
table = soup.find('table')

# Extract table headers
headers = [header.text.strip() for header in table.find_all('th')][1:]

# print(headers)

# Extract table rows
data = []
for row in table.find_all('tr')[1:]:
    row_data = [cell.text.strip() for cell in row.find_all('td')]
    # print(row_data)
    if(row_data != []):
        data.append(row_data)

# Create DataFrame
df = pd.DataFrame(data, columns=headers)

# delete rows, where the string in column "Ende" doesnt include "2024"
df = df[~df['Ende'].str.contains('2024')]

# get just the first two columns (Stationsname and Stations_id)
df_important = df[['Stationsname', 'Stations_ID', 'Breite', 'Länge']]

# delete all duplicated rows
df_important.drop_duplicates(subset='Stationsname', keep='first', inplace=True)

# I want to reduce tha data to 500 rows. The data should be reduced by deleting rows where the Breite and Länge are closest to each other
# Assuming df is your DataFrame with columns ['Stationsname', 'Stations_ID', 'Breite', 'Länge']
# Convert Breite and Länge to radians for distance calculation

df_important['Breite'] = df_important['Breite'].astype(float)
df_important['Länge'] = df_important['Länge'].astype(float)

df_important['Breite_rad'] = df_important['Breite'] * (3.141592653589793 / 180)
df_important['Länge_rad'] = df_important['Länge'] * (3.141592653589793 / 180)

# Create input for KMeans clustering
X = df_important[['Breite_rad', 'Länge_rad']]

# Specify the number of clusters (desired number of rows after reduction)
num_clusters = 500

# Perform KMeans clustering
kmeans = KMeans(n_clusters=num_clusters, random_state=42)
df_important['cluster'] = kmeans.fit_predict(X)

# Compute the centroid of each cluster
centroids = pd.DataFrame(kmeans.cluster_centers_, columns=['Breite_rad', 'Länge_rad'])

# Find the nearest point in each cluster to its centroid
nearest_points = []
for cluster_label, centroid in centroids.iterrows():
    cluster_points = df_important[df_important['cluster'] == cluster_label]
    distances = ((cluster_points['Breite_rad'] - centroid['Breite_rad']) ** 2 + 
                 (cluster_points['Länge_rad'] - centroid['Länge_rad']) ** 2) ** 0.5
    nearest_point_idx = distances.idxmin()
    nearest_points.append(nearest_point_idx)

# Keep only the nearest points
reduced_df = df_important.loc[nearest_points]

# Drop the cluster column and radians columns
reduced_df.drop(['cluster', 'Breite_rad', 'Länge_rad'], axis=1, inplace=True)

print(reduced_df)

# Create a map
# Create a map centered at a specific location
mymap = folium.Map(location=[0, 0], zoom_start=2)

# Add markers for specific locations
locations = reduced_df[['Breite', 'Länge']].values

for loc in locations:
    folium.Marker(location=loc).add_to(mymap)

# Save the map to an HTML file
mymap.save("map_reduced.html")