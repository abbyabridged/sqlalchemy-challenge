###########################
# Dependencies
###########################

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect, distinct

from flask import Flask

###########################
# Database setup
###########################

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect an existing database into a new model
Base = automap_base()

# Reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

###########################
# Flask setup
###########################

# Create an app, pass name
app = Flask(__name__)

###########################
# Flask routes
###########################

# Define action when user hits index route
## List all the routes that are available
@app.route("/")
def homepage():
    return (
        f"Welcome to Climate App!<br>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/startdate<br/>"
        f"/api/v1.0/startdate/enddate<br/>"
    )

# @app.route("api/v1.0/precipitation")
## Convert the query results to a dictionary using date as the key and prcp as the value.
## Return the JSON representation of your dictionary.


# @app.route("api/v1.0/stations")
## Return a JSON list of stations from the dataset.

# @app.route("api/v1.0/tobs")
## Query the dates and temperature observations of the most active station for the last year of data (2015 to 2016? As in the year before the last year of data?)
## Return a JSON list of temperature observations (TOBS) for the previous year.


# @app.route("api/v1.0/<start>")
## Return a JSON list of the min temp, average temp and max temp for a given start or start-end range.
## When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.


# @app.route("api/v1.0/<start>/<end>")
## Return a JSON list of the min temp, average temp and max temp for a given start or start-end range.
## When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.


if __name__ == "__main__":
    app.run(debug=True)