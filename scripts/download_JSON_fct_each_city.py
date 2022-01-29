# This script downloads the forecast for each city of the selected country csv.
# A population filter can be applied if variable not None.
# Shall be run once a week (eg:Thursdays), to not overwhelm met.no servers

from src.generate_cities_db import *
from src.retrieve_forecast_methods import *
import pandas as pd
import os
from datetime import date
import requests as rq



country_name = 'Netherlands'
country_csv = '{}.csv'.format(country_name.lower())
population_filter = 30 # None if all

# Try to read country_name.csv if it already exists, otherwise create it and read.
try:
    df = pd.read_csv('../db/'+country_csv)
except FileNotFoundError:
    print('{} not found. Create it!'.format(country_csv))
    df = generate_countryDB(country_name)

print('apply pop filter')
# Apply population filter to the country csv
df_filtered_cities = filter_cities_by_population(df, population_filter)
df_filtered_cities.to_csv('../db/filtered/{}_filtered_cities.csv'.format(country_name))

print('download JSON for each')
# Download JSON forecast for each city on the df_filtered_cities database
for index, row in df_filtered_cities.iterrows():
    print(row['city'])
    # Declaring params
    params = dict(lat = str(row['lat']),
                  lon = str(row['lng']),
                  altitude = '30')
    # Retrieving forecast
    r = retrieve_fct(params)
    filename = '../city_fct/'+row['city']+'.json'
    save_json(r, filename)

# Create unified DF with all forecasted cities
print('create unified DF')
df_unified = pd.DataFrame(columns=['city','date', 'time', 'air_temperature', 'cloud_area_fraction',
               'relative_humidity', 'weekday'])

# Read json and append the city forecast to the unified DataFrame
for city_json in os.listdir('../city_fct/'):
    print(city_json)
    
    # Json to df
    filename = '../city_fct/'+city_json
    data_file = open_json_file(filename)
    df1 = create_df_from_JSON(data_file)
    df2 = clean_data(df1)
    df2['city'] = city_json.split('.')[0]
    
    # Unify df
    #df_unified = df_unified.append(df2[['city','date', 'time', 'air_temperature', 'cloud_area_fraction',
    #           'relative_humidity', 'weekday']])
    df_temp = df2[['city','date', 'time', 'air_temperature', 'cloud_area_fraction','relative_humidity', 'weekday']]
    df_unified = pd.concat([df_unified, df_temp])
    
# Reset index of the unified dataframe
df_unified = df_unified.reset_index(drop=True)
df_unified.to_csv('../db/unified/{}_unified_{}.csv'.format(country_name,date.today()))

print('\n\nDONE')