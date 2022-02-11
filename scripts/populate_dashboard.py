import pandas as pd
from datetime import date, timedelta
from os import listdir
from geopy.distance import geodesic
import re

country_name = 'Netherlands'
today = date.today()
origin = (52.0929, 4.2935) # Data from LEIDEN

# Find the most recent final database for the country
list_unified = listdir('../db/final')
country_db_list = [entry for entry in list_unified if country_name in entry]
most_recent = country_db_list[-1]
# Read the most recent final df
df_recent = pd.read_csv('../db/final/{}'.format(most_recent), index_col=0)

## CALCULATE DISTANCES
# Create list of coordinate tuples of the cities (destinations)
destinations = list(zip(df_recent['lat'],df_recent['lng']))
# Calculate distance between coordinates using geodesic and save it to a column
df_recent['distance'] = [geodesic(origin, coords).km for coords in destinations]
df_recent['distance'] = df_recent['distance'].astype(int)
df_recent['distance'] = df_recent['distance'].astype(str) + ' km'

# Select relevant columns to render
df_selected = df_recent[['city','date','air_temperature','distance','cloud_area_fraction']].copy()
df_selected['date'] = df_selected['date'].str.replace(' 00:00:00','')

# Render the df as html
table = df_selected.to_html(index=False,header=False, max_rows = 10)
# Use regex to select only the rows of the html
tbody = re.findall('<tbody>\n([^"]*)</tbody>',table)[0]



## POPULATING THE TEMPLATE
with open('../dashboard/template.html','r') as f:
    template = f.read()

# Find next saturday (a bit ugly but it works)
days_to_weekend = 5 - date.today().weekday()
next_saturday = date.today() + timedelta(days_to_weekend)
next_sunday = next_saturday + timedelta(1)


# Populate table
template = template.replace('{TABLE_TO_BE_POPULATED}',tbody)
# Populate dates
template = template.replace('{DATE1}',next_saturday.isoformat())
template = template.replace('{DATE2}',next_sunday.isoformat())

# Most recent map file
list_unified = listdir('../plots')
maps_list = [entry for entry in list_unified if country_name in entry]
most_recent_map = maps_list[-1]
# Populate map
template = template.replace('{MAP_FILE.HTML}','../plots/'+most_recent_map)

with open('../dashboard/index.html','w') as f:
    f.write(template)

print('Dashboard populated')