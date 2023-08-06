# gtempco2

gtempco2 is a PyPI application to display global temperature and co2 of land and ocean with NOAA datasets.

NOAA monthly datasets on the global temperature of land and ocean and the global co2 will be automatically downloaded. 

gtempco2 is to plot a graph for a user-specified time period with two lines representing global temperature and global CO2 levels. The graph includes first-order regression lines with coefficients and R-squared values.

To install gtempco2, use the following pip command.

$ pip install gtempco2

To run gtempco2, the user-specified time period such as start-date and end-date is needed to plot a graph of the global temperature and co2 from start-date to end-date. 

The format of them is as follows.

For example, 1958-03 indicates March 1958 when NOAA started the measurement of the global co2.

<pre>
$ gtempco2
enter start_date: e.g. 1960-04
co2 measurement started from 1958-03
yyyy-mo: 1960-06
enter end_date: e.g. 2023-04
yyyy-mo: 1965-06
start_date= 1960-06 end_date= 1965-06
</pre>

The system will ask the start-date and end-date. The result will be shown and saved in the directory as follows.

<img src='https://github.com/ytakefuji/gtempco2/raw/main/1960-06_1965-06.png' height=450 width=600>

