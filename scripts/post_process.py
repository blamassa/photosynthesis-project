# This scripts uses the df_unified generated by the auto-run script 'download_JSON_fct_each_city.py'.
# The purpuse of the script is to rank the cities based on the cloud_area_fraction, insert the population and generate an html plot.
# This could be substituted by a plotly dashboard in the future.
from datetime import date
from src.postprocess_forecast_methods import *
from os import listdir
import pandas as pd

country_name = 'Netherlands'
today = date.today()
cloud_area_threshold = 30

# Find the most recent unified database for the country
list_unified = listdir('../db/unified')
country_db_list = [entry for entry in list_unified if country_name in entry]
most_recent = country_db_list[-1]

# Read the unified df
df_unified = pd.read_csv('../db/unified/{}'.format(most_recent))

## Rank forecast for next weekend and filter cloud area fraction
df_cloud_median = ranking_fct_next_weekend(df_unified)
df_cloud_median.to_csv('../db/forecast/{}_{}.csv'.format(country_name, today))

# Join the final filtered forecast dataframe to the population for plotting
df_forecast_populated = join_population_final_forecast(df_cloud_median, country_name)

# Generate plot
generate_plot(df_plot = df_forecast_populated, country_name = country_name)