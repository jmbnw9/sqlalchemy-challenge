import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

session = Session(engine)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

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
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br>"
        f"/api/v1.0/<start><br>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def prcp():
    one_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    data = (session.query(Measurement.date, Measurement.prcp).filter(Measurement.date > one_year).order_by(Measurement.date).all())

    measurements = []
    for date, prcp in data:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        measurements.append(prcp_dict)

    return jsonify(measurements)

@app.route("/api/v1.0/stations")
def name():
    active_stations = (session.query(Measurement.station, func.count(Measurement.station)).\
                   group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all())

    active_stations

    stations = []
    for station in active_stations:
        name_dict = {}
        name_dict["station"] = station
        stations.append(name_dict)
        
    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def temperature():
    temp = session.query(Measurement.tobs).filter(Measurement.station =='USC00519281').filter(Measurement.station > one_year).all()

    temperatures = []
    for temps in temp:
        temperature_dict = {}
        temperature_dict["tobs"] = temp
        temperature.append(temperature_dict)

    return jsonify(temperature)

if __name__ == '__main__':
    app.run(debug=True)
