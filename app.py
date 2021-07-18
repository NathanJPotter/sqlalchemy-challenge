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
        f"/api/v1.0/start<br/>"
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

@app.route("/api/v1.0/start")
def start_date_temps(start):

    """Query the  min temp, the av temp, and the max temp from a given start date."""
    start = datetime.strptime('2016-08-23', '%Y-%m-%d').date()
    start_results = session.query(func.avg(Measurement.tobs),func.max(Measurement.tobs),func.min(Measurement.tobs).\
               filter(Measurement.date >= start)
    start_tobs_list = []   
    for i in start_results:
        dict = {}
        dict["TMIN"] = float(tobs[1])                     
        dict["TMAX"] = float(tobs[0])
        dict["TAVG"] = float(tobs[2])
        start_tobs_list.append(dict)
    return jsonify(start_tobs_list)  


@app.route("/api/v1.0/start/end")
def start_end_dates(start, end):
    
    """Query the  min temp, the av temp, and the max temp for a given start or start-end range."""
    start = datetime.strptime('2016-08-23', '%Y-%m-%d').date()                      
    end = datetime.strptime('2017-08-23', '%Y-%m-%d').date()
    end_results = session.query(func.avg(Measurement.tobs),func.max(Measurement.tobs),func.min(Measurement.tobs).\
            filter(Measurement.date >= start)                     
    start_end_tobs_list = []
    for i in start_end_tobs_list:
        dict = {}
        dict["TMIN"] = float(tobs[1])                     
        dict["TMAX"] = float(tobs[0])
        dict["TAVG"] = float(tobs[2])
        start_end_tobs_list.append(dict)
    return jsonify(start__end_tobs_list) 

if __name__ == "__main__":
    app.run(debug=True)
