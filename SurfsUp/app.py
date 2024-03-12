# Import the dependencies.
from flask import Flask, jsonify
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

import datetime as dt


#################################################
# Database Setup
#################################################


# reflect an existing database into a new model
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB
session_var = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        "<h2>Available Routes for the 'hawaii.sqlite' Dataset created with Flask:</h2><br/>"
        "<h3>List of Precipitation Analysis Results for the last 12 months:</h3><br/>"
        f"/api/v1.0/precipitation<br/><br/>"
        "<h3>List of stations from the dataset hawaii.sqlite:</h3><br/>"
        f"/api/v1.0/stations<br/><br/>"
        "<h3>Dates and temperature observations of the most active station, for last 12 months:</h3><br/>"
        f"/api/v1.0/tobs<br/><br/>"
        "<h3>List of min/max/avr temps for a specified start range:</h3><br/>"
        f"Be sure to follow this format: http://127.0.0.1:5000/api/v1.0/2017-06-23<br/>"
        f"YYYY-MM-DD for the start date. The last date in the database will show automatically.<br/>"
        f"/api/v1.0/&lt;start&gt;<br/><br/>"
        "<h3>List of min/max/avr temps for a specified start-end range:</h3><br/>"
        f"Be sure to follow this format: http://127.0.0.1:5000/api/v1.0/2017-06-30/2017-07-03<br/>"
        f"YYYY-MM-DD for both start and end dates<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;"
    )

@app.route("/api/v1.0/precipitation")

def precipitation():
    """Return a list of the precipitation analysis"""
    # session link
    session_var = Session(engine)

    # Most recent date in the data set
    most_recent_date = session_var.query(measurement.date).order_by(measurement.date.desc()).first()[0]

    # Date one year from last date in dataset
    last_year_date = dt.datetime.strptime(most_recent_date, '%Y-%m-%d').date() - dt.timedelta(days=365)

    # Perform a query to retrieve the data and precipitation scores (date and prcp)
    precipitation_data = session_var.query(measurement.date, func.avg(measurement.prcp)).\
        filter(measurement.date >= last_year_date).\
        group_by(measurement.date).all()

    # Convert the query results into a dictionary
    precipitation_dict = {}
    for date, prcp in precipitation_data:
        precipitation_dict[date] = prcp

    # Close the session
    session_var.close()

    # Return the JSON representation of the dictionary
    return jsonify({"Date and Precipitation for 1 year prior to last date in database": precipitation_dict})

@app.route("/api/v1.0/stations")


