# SQL Alchemy

![Surf](Images/hawaii_surf.jpg)

## Climate Analysis and Engineering
Uses SQLAlchemy to access a sqlite database to perform data exploration and analysis

### Precipitation Analysis
Retrieves the last 12 months of data and plots precipitation by date.

### Station Analysis
1. Returns the amount of stations in the dataset 
2. Determines the most active station
2. Plots the temperatures recorded for the most active station


## Climate App
Uses Flask to create the following routes:

* / - Home page
* /api/v1.0/precipitation - Returns precipitation analysis query results
* /api/v1.0/stations - Returns a list of stations
* /api/v1.0/tobs - Returns temperature observations from the most active station
* /api/v1.0/&#60;start&#62; and /api/v1.0/&#60;start&#62;/&#60;end&#62; - Returns the minimum, maximum and average temperature for a given start and end date (end date is optional.)
