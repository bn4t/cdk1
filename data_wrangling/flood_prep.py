import geopandas as gpd
import contextily as ctx
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import pandas as pd
import ast  # Zum sicheren Umwandeln von Strings in Listen/Tuples
from opencage.geocoder import OpenCageGeocode

pd.set_option('display.width', 2000)

# Daten einlesen
hanze = pd.read_csv(r'../data/source/hanze_all.csv', sep=',')
hanze_regions = pd.read_csv(r'../data/source/regioncodes.csv', sep=',')


# Unnötige Spalten löschen
hanze = hanze.drop(columns=['Country code', 'Flood source', 'Regions affected (v2010)', 'Area flooded', 'Persons affected', 'Losses (nominal value)', 'Losses (original currency)', 
                            'Notes', 'Changes'])

# Spalten umbenennen
hanze = hanze.rename(columns={'Regions affected (v2021)': 'regions'})
hanze = hanze.rename(columns={'Losses (2020 euro)': 'Losses (mln EUR, 2020)'})

new_column_order = [
    'ID', 'Year', 'Country name', 'Start date', 'End date', 'Type', 'regions', 'Cause', 'References', 'Fatalities', 'Losses (mln EUR, 2020)'
]

hanze = hanze[new_column_order]

# Länder filtern
countries = ['France', 'Switzerland', 'Liechtenstein', 'Monaco', 'Slovenia', 'Austria', 'Germany', 'Italy']
hanze_filtered = hanze[hanze['Country name'].isin(countries)]
hanze_filtered = hanze_filtered[(hanze_filtered['Year'] >= 1979) & (hanze_filtered['Year'] <= 2023)]

# Regionen filtern
countries_diff = ['FR', 'CH', 'LI', 'MC', 'SI', 'AT', 'DE', 'IT']
regions_filtered = hanze_regions[hanze_regions['Code'].str[:2].isin(countries_diff)]

print(hanze_filtered)
print(regions_filtered)
################################################################### Koordinaten einfügen

key = 'e6b40f80dcff475dae09c9c4d1e7985e'  # Replace with your actual OpenCage API key
geocoder = OpenCageGeocode(key)

# Function to get coordinates
def get_coordinates(place_name):
    result = geocoder.geocode(place_name)
    if result:
        return result[0]['geometry']['lat'], result[0]['geometry']['lng']
    else:
        return None, None
    

# Apply the get_coordinates function to the 'Name' column
regions_filtered['Coordinates'] = regions_filtered['Name'].apply(lambda x: get_coordinates(x))



print(regions_filtered.head)

output_path = r"C:\Users\Murat Kayhan\OneDrive - FHNW\Documents\FHNW\ckd\Data\regionswithcords.csv"
regions_filtered.to_csv(output_path, index=False)

###########################################################################################################################
#Codes durch Koordinaten ersetzen

regions_filtered = pd.read_csv(r'C:\Users\Murat Kayhan\OneDrive - FHNW\Documents\FHNW\ckd\Data\regionswithcords.csv')

print(regions_filtered)
regions_mapping = regions_filtered.set_index('Code')['Coordinates'].to_dict()

# Define a function to replace region codes with their corresponding coordinates
def replace_codes_with_coordinates(codes):
    if pd.isna(codes):
        return codes
    codes_list = codes.split(';')
    coordinates_list = [regions_mapping.get(code, code) for code in codes_list]
    return ';'.join(coordinates_list)

# Apply this function to the 'Regions affected (v2021)' column in the hanze dataset
hanze_filtered['regions'] = hanze_filtered['regions'].apply(replace_codes_with_coordinates)

# Display the first few rows of the updated 'Regions affected (v2021)' column to verify the changes
print(hanze_filtered[['regions']].head())


output_path = r"C:\Users\Murat Kayhan\OneDrive - FHNW\Documents\FHNW\ckd\Data\hanze_without_cords.csv"
hanze_filtered.to_csv(output_path, index=False)

###########################################################################################################################
# Neue Zeilen für jede Region erstellen

hanze_filtered = pd.read_csv(r'C:\Users\Murat Kayhan\OneDrive - FHNW\Documents\FHNW\ckd\Data\hanze_without_cords.csv')


expanded_data = hanze_filtered.assign(regions=hanze_filtered['regions'].str.split(';')).explode('regions')
print(expanded_data[['ID', 'regions']].head())

output_path = r"C:\Users\Murat Kayhan\OneDrive - FHNW\Documents\FHNW\ckd\Data\hanze_with_cords.csv"
expanded_data.to_csv(output_path, index=False)
##########################################################################################################################
hanzewithcords = pd.read_csv(r'C:\Users\Murat Kayhan\OneDrive - FHNW\Documents\FHNW\ckd\Data\hanze_with_cords.csv')
print(hanzewithcords[['regions']].head())

rain_related = hanzewithcords[hanzewithcords['Cause'].str.contains('rain', case=False, na=False)]
print(hanzewithcords[['Cause']].head())
print(hanzewithcords)

output_path = r"C:\Users\Murat Kayhan\OneDrive - FHNW\Documents\FHNW\ckd\Data\flood_data_fixed_everything.csv"
hanzewithcords.to_csv(output_path, index=False)

#########################################################################################################################
#Spalte Latitude und Longitude

import pandas as pd

# Load the provided CSV file
flood_data = pd.read_csv(r'C:\Users\Murat Kayhan\OneDrive - FHNW\Documents\FHNW\ckd\Data\flood_data_fixed_everything.csv')

print(flood_data)

# Identify and filter out invalid entries in the 'regions' column
valid_entries = flood_data[flood_data['regions'].str.contains('^\d+\.\d+,\s*\d+\.\d+$', regex=True)].copy()

# Split the valid 'regions' column into 'Latitude' and 'Longitude' columns
valid_entries[['Latitude', 'Longitude']] = valid_entries['regions'].str.split(',', expand=True)

# Convert to numeric values
valid_entries['Latitude'] = pd.to_numeric(valid_entries['Latitude'])
valid_entries['Longitude'] = pd.to_numeric(valid_entries['Longitude'])

print(valid_entries[['Latitude', 'Longitude']].head())

# Save the updated dataframe to a new CSV file
valid_entries.to_csv('path_to_your_file/flood_data_with_lat_long_valid.csv', index=False)

#########################################################################################3
#Spalten neu anordnen

cols = valid_entries.columns.tolist()
end_date_index = cols.index('End date')
new_order = cols[:end_date_index + 1] + ['Latitude', 'Longitude'] + cols[end_date_index + 1:-2]
valid_entries = valid_entries[new_order]

print(valid_entries.columns)

output_path = r"C:\Users\Murat Kayhan\OneDrive - FHNW\Documents\FHNW\ckd\Data\flood_data_fixed_everything_mitSpalte.csv"
valid_entries.to_csv(output_path, index=False)
