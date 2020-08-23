###########################
# Dependencies
###########################

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect, distinct

import datetime as dt

from flask import Flask, jsonify

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
        f"/api/v1.0/start_date<br/>"
        f"/api/v1.0/start_date/end_date"
    )

@app.route("/api/v1.0/precipitation")
## Convert the query results to a dictionary using date as the key and prcp as the value.
## Return the JSON representation of your dictionary.
def precipitation():

    # Create session (link) from Python to DB
    session =  Session(engine)

    # Return precipitation data including date and prcp
    data = session.query(Measurement.date, Measurement.prcp).all()
    session.close()

    # Create a dictionary from the data and append to a list
    precipitation_data = []
    for date, prcp in data:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["prcp"] = prcp
        precipitation_data.append(precipitation_dict)
    # Return the result
    return jsonify(precipitation_data)

## Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    data = session.query(Station.id,Station.station,Station.name,Station.latitude,Station.longitude,Station.elevation).all()
    session.close()

    station_data = []
    for id, station, name, latitude, longitude, elevation in data:
        station_dict = {}
        station_dict["id"] = id
        station_dict["station"] = station
        station_dict["name"] = name
        station_dict["latitude"] = latitude
        station_dict["longitude"] = longitude
        station_dict["elevation"] = elevation
        station_data.append(station_dict)
    return jsonify(station_data)

## Query the dates and temperature observations of the most active station for the last year of data
## Return a JSON list of temperature observations (TOBS) for the previous year.
@app.route("/api/v1.0/tobs")
def tobs_USC00519281():
    session = Session(engine)
    data = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == "USC00519281").filter(Measurement.date >= (dt.date(2017,8,23) - dt.timedelta(days=365))).all()
    session.close()
    tobs_USC00519281_data  = []
    for date, tobs in data:
        tobs_USC00519281_dict = {}
        tobs_USC00519281_dict["date"] = date
        tobs_USC00519281_dict["tobs"] = tobs
        tobs_USC00519281_data.append(tobs_USC00519281_dict)
    return jsonify(tobs_USC00519281_data)

## Return a JSON list of the min temp, average temp and max temp for a given start or start-end range.
## When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
@app.route("/api/v1.0/<start>")
def date_single(start):
    start_date = dt.datetime.strptime(start,"%Y-%m-%d")
    session = Session(engine)
    sel = [func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)]
    data = session.query(*sel).filter(func.strftime("%Y-%m-%d", Measurement.date) >= start).all()
    session.close()
    return jsonify(data)

## Return a JSON list of the min temp, average temp and max temp for a given start or start-end range.
## When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
@app.route("/api/v1.0/<start>/<end>")
def date_range(start,end):
    start_date = dt.datetime.strptime(start,"%Y-%m-%d")
    end_date = dt.datetime.strptime(end,"%Y-%m-%d")
    session = Session(engine)
    sel = [func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)]
    data = session.query(*sel).\
    filter(func.strftime("%Y-%m-%d", Measurement.date) >= start).\
    filter(func.strftime("%Y-%m-%d", Measurement.date) <= end).all()
    session.close()
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)