# Import libraries
import datetime as dt
import numpy as np 
import pandas as pd 

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import inspect, create_engine, func

from flask import Flask, jsonify

#############################################
# Database Setup
#############################################

# Create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#############################################
# Flask Set up
#############################################
app = Flask(__name__)

#############################################
#Flask Routes
#############################################
@app.route("/")
def welcome():
    return (
        f"Welcome to the Hawaii Climate Analysis API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start/end"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return the precipitation data for the last year"""
    # Calculate the date one year from the last date in data set
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # Query for the date and precipitation data for the last year
    precipitation =  session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= prev_year).all()

    # Dict with date as the key ad prcp as the value
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)

@app.route("/api/v1.0/stations")
def stations():
    """Return the most active stations that have the most data"""
    # List the stations and the counts in descending order
    station_activity = (session.query(Measurement.station, func.count(Measurement.station))\
                        .group_by(Measurement.station)\
                        .order_by(func.count(Measurement.station).desc())\
                        .all())
    return jsonify(station_activity)

@app.route("/api/v1.0/tobs")
def temperature_observations():
    """Query the dates and temperature observations of the most active station for the last year of data"""
    # Get the last 12 months of temperature data for the most active station
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    station_activity = (session.query(Measurement.station, func.count(Measurement.station))\
                        .group_by(Measurement.station)\
                        .order_by(func.count(Measurement.station).desc())\
                        .all())

    active_station_ID = station_activity[0][0]
    
    temp_data = (session.query(Measurement.date, Measurement.tobs)\
                   .filter(Measurement.date >= prev_year)\
                   .filter(Measurement.station == active_station_ID)\
                   .order_by(Measurement.date)\
                   .all())
    return jsonify(temp_data)

@app.route("/api/v1.0/start/end")
def start_end_dates():

    """Query the  min temp, the av temp, and the max temp for a given start-end range."""
    station_activity = (session.query(Measurement.station, func.count(Measurement.station))\
                        .group_by(Measurement.station)\
                        .order_by(func.count(Measurement.station).desc())\
                        .all())

    active_station_ID = station_activity[0][0]
    
    active_stationName = (session.query(Station.name)\
                      .filter_by(station = active_station_ID))
    active_stationName = active_stationName[0][0]

    lowest_temp = (session.query(Measurement.tobs).\
               filter(Measurement.station == active_station_ID).\
               order_by(Measurement.tobs.asc()).\
               first())
    lowest_temp = lowest_temp[0]

    av_temp = (session.query(func.avg(Measurement.tobs))\
                  .filter(Measurement.station == active_station_ID))
    av_temp = '{0:.3}'.format(av_temp[0][0])

    highest_temp = (session.query(Measurement.tobs).\
               filter(Measurement.station == active_station_ID).\
               order_by(Measurement.tobs.desc()).\
               first())
    highest_temp = highest_temp[0]

    start_end_results = (f"Key temperatures (in degrees Farenheit) at {active_stationName} are: min = {lowest_temp}, av = {av_temp} and max = {highest_temp}")

    return jsonify(start_end_results)

if __name__ == "__main__":
    app.run(debug=True)
