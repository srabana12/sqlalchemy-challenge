# sqlalchemy-challenge

<b>Precipitation Analysis</b>

The precipitation analysis retrieves the most recent date in the data set and calculates the date one year from the last date. The script then performs a query to retrieve the precipitation data for the last 12 months and saves the query results as a pandas DataFrame. The DataFrame is sorted by date and plotted using Pandas Plotting with Matplotlib. Finally, the script uses Pandas to calculate summary statistics for the precipitation data, including the count, mean, standard deviation, minimum, 25th percentile, median, 75th percentile, and maximum values.


<b>Station Analysis</b>

The station analysis calculates the total number of stations in the dataset and identifies the most active stations, listed in descending order of the number of rows in the dataset. The script then calculates the lowest, highest, and average temperature for the most active station.


<b>Climate App</b>

The welcome() route provides a list of available routes, including <br>
/api/v1.0/precipitation, which returns the precipitation data for the last 12 months,  <br>
/api/v1.0/stations, which returns a list of all the weather stations, and  <br>
/api/v1.0/tobs, which returns the temperature data for the last year for the station with the highest number of observations.

The /api/v1.0/start/end route allows the user to specify a start and end date range and returns the minimum, maximum, and average temperatures for that range. If only a start date is specified, the route returns the same temperature statistics for all dates from the start date to the last date in the database.

This API is a useful tool for exploring and analyzing the climate data for Hawaii. The precipitation() route allows users to quickly obtain precipitation data for a given time period, while the tobs() route provides temperature data for the station with the highest number of observations. The /api/v1.0/start/end route allows users to compare temperature data for different time periods, which could be useful for trend analysis and climate modeling.
