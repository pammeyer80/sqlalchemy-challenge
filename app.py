# import statements
from scipy import stats 
from statistics import mean
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
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Routes
#################################################

@app.route("/")
def welcome():
    return (
        f"Welcome to the Climate App<br/>"
        f"Available Routes:<br/>"
        f"  /api/v1.0/precipitation<br/>"
        f"  /api/v1.0/stations<br/>"
        f"  /api/v1.0/tobs<br/><br/>"
        f"For the following routes start and end dates should be formatted <strong>yyyy-mm-dd</strong>. End date is optional.<br>"
        f"  /api/v1.0/&#60;start&#62;<br/>"
        f"  /api/v1.0/&#60;start&#62;/&#60;end&#62;<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all precipitation scores in the last 12 months
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date>='2016-08-23', Measurement.prcp!="None").order_by(Measurement.date).all()

    session.close()

    # Create a dictionary from the row data and append to a list of prcp_scores
    prcp_scores = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict[date] = prcp
        prcp_scores.append(prcp_dict)

    return jsonify(prcp_scores)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all precipitation scores in the last 12 months
    results = session.query(Station.station).all()

    session.close()

    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all precipitation scores in the last 12 months
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station=='USC00519281', Measurement.date>='2016-08-23', Measurement.tobs!="None").order_by(Measurement.date).all()

    session.close()

    # Create a dictionary from the row data and append to a list of prcp_scores
    tobs_all = []
    for date, tobs in results:
        tobs_dict = {}
        tobs_dict[date] = tobs
        tobs_all.append(tobs_dict)

    return jsonify(tobs_all)


@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def stats_start(start, end=None):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    if end == None:
        # Query temperatures since the start date
        results = session.query(Measurement.tobs).filter(Measurement.date>=start, Measurement.tobs!="None").all()
    else:
        # Query temperatures between start and end date
        results = session.query(Measurement.tobs).filter(Measurement.date>=start, Measurement.date<=end,Measurement.tobs!="None").all()
#     
    session.close()

    results_ls = [result[0] for result in results]

    stats_all = []
    stats_dict = {}
    stats_dict["Minimum Temp"] = stats.tmin(results_ls)
    stats_dict["Maximum Temp"] = stats.tmax(results_ls)
    stats_dict["Average Temp"] = round(stats.tmean(results_ls), 2)
    stats_all.append(stats_dict)

    return jsonify(stats_all)



if __name__ == "__main__":
    app.run(debug=True)
