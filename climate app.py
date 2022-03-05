
import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Create an engine for the database
engine = create_engine("sqlite:///Resources/hawaii.sqlite", echo=False)

# Reflect Database into ORM classes
Base = automap_base()
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create session (link) from Python to the DB
session = Session(engine)

# Flask Setup

app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"Precipitation: /api/v1.0/precipitation<br/>"
        f"List of all Stations: /api/v1.0/stations<br/>"
        f"Temperature for the most active station for one year: /api/v1.0/tobs<br/>"
        f"Temperature information from the start date(start): /api/v1.0/yyyy-mm-dd<br/>"
        f"Temperature information from start to end dates(start/end): /api/v1.0/yyyy-mm-dd/yyyy-mm-dd"
    )


    
@app.route("/api/v1.0/precipitation")
def precipitation():
  
   # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query for the dates and precipitation values
    results =   session.query(Measurement.date, Measurement.prcp).\
                order_by(Measurement.date).all()

    # Convert to list of dictionaries to jsonify
    prcp_date_list = []

    for date, prcp in results:
        new_dict = {}
        new_dict[date] = prcp
        prcp_date_list.append(new_dict)

    session.close()

    return jsonify(prcp_date_list)

@app.route("/api/v1.0/stations")
    
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    stations = {}

    # Query all stations
    results = session.query(Station.station, Station.name).all()
    for s,name in results:
        stations[s] = name

    session.close()
 
    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
  
  results = session.query(Measurement.tobs).\
        filter(Measurement.station == "USC00519281").\
        filter(Measurement.date >= "2016-08-23").\
        filter(Measurement.date <= "2017-08-23").all()

 

  tob = list(np.ravel(results))

  session.close()

  return jsonify(tob)


@app.route("/api/v1.0/yyyy-mm-dd")

def temp_info ():

    results = session.query(func.avg(Measurement.tobs),func.min(Measurement.tobs),func.max(Measurement.tobs)).\
    filter(Measurement.date >= "2016-08-23").all()

    data = list(np.ravel(results))

    session.close()

    return jsonify(data)

@app.route("/api/v1.0/yyyy-mm-dd/yyyy-mm-dd")
def start_end():
   
    results = session.query(func.avg(Measurement.tobs),func.min(Measurement.tobs),func.max(Measurement.tobs)).\
    filter(Measurement.date >= "2016-08-23").\
    filter(Measurement.date <= "2017-08-23").all()

    data1 = list(np.ravel(results))

    session.close()

    return jsonify(data1)

if __name__ == '__main__':
    app.run()