# Import libraries
import datetime as dt
import numpy as np 
import pandas as pd 

import sqlaclchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from aqlalchemy import inspect, create_engine, func

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
    return