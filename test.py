import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


engine = create_engine("sqlite:///Resources/hawaii.sqlite")


Base = automap_base()
Base.prepare(engine, reflect=True)


Measurement = Base.classes.measurement
Station = Base.classes.station


session = Session(engine)

app = Flask(__name__)


@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        "Available Routes:<br/>"
        "/api/v1.0/precipitation<br/>"
        "/api/v1.0/stations<br/>"
        "/api/v1.0/tobs"
    )


@app.route("/api/v1.0/precipitation")
def precip():
    """Return a list of all precipitation results by date"""

    results = session.query(Measurement.date, func.max(Measurement.prcp)).\
                filter(Measurement.date >= '2016-08-24').\
                group_by(Measurement.date).all()


    all_precip = []
    for precip in results:
        precip_dict = {}
        precip_dict['date'] = precip[0]
        precip_dict['prcp'] = precip[1]
        all_precip.append(precip_dict)

    return jsonify(all_precip)



@app.route("/api/v1.0/stations")
def stations():
    """Return a json list of stations from the dataset"""

    results = session.query(Station.station, Station.name).group_by(Station.station).all()


    all_stations = []
    for station in results:
        station_dict = {}
        station_dict["station_id"] = station[0]
        station_dict["station_name"] = station[1]
        all_stations.append(station_dict)

    return jsonify(all_stations)


@app.route("/api/v1.0/tobs")
def tobs():
    """Return a JSON list of Temperature Observations (tobs) for the previous year"""
   
    results = session.query(Measurement.station, func.count(Measurement.tobs)).\
    filter(Measurement.date >= '2016-08-24').\
    group_by(Measurement.station).\
    order_by(func.count(Measurement.tobs).desc()).all()

    
    all_tobs = []
    for tobs in results:
        tobs_dict = {}
        tobs_dict["station"] = tobs[0]
        tobs_dict["temp_observations"] = tobs[1]
        all_tobs.append(tobs_dict)

    return jsonify(all_tobs)




if __name__ == '__main__':
    app.run(debug=True)
