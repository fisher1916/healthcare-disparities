import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
station = Base.classes.station
measurement = Base.classes.measurement

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
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temperature/start/end"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create session (link) from Python to the DB
    session = Session(engine)

    """Return a list of a dicionary for precipitation"""
    # Query all for precipitation
    results = session.query(measurement.date,measurement.prcp).all()
    prcp_dict={date:prcp for date, prcp in results}
    session.close()

    return jsonify(prcp_dict)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of stations"""
    # Query all stations
    results = session.query(station.station).all()

    session.close()

    return jsonify(results)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of temp observations"""
    # Query all temp last year of most active station
    last_year = dt.date(2017,8,23)-dt.timedelta(days = 365)
    results = session.query(measurement.tobs).filter(measurement.date >= last_year).filter(measurement.station == "USC00519281").all()

    session.close()

    return jsonify(results)

@app.route("/api/v1.0/temperature/<start>/<end>")
def temperature(start,end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of min, max, avg with the ability to enter dates from the api"""
    # Query all all station data
    results = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).filter(measurement.date>=start).filter(measurement.date<=end).all()
    session.close()

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
