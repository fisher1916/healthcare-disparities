import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify, render_template

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///data/cms.db")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Cms = Base.classes.cms

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    return render_template("map.html")


@app.route("/mortality")
def mortality():
    # Create session (link) from Python to the DB
    session = Session(engine)

    """Return a list of a dicionary for mortality"""
    # Query all for mortality
    results = session.query(
        Cms.state,
        Cms.state_name,
        Cms.facility_name,
        Cms.measure_name,
        Cms.score,
        Cms.percent_poverty,
        Cms.percent_veteran,
        Cms.percent_married,
        Cms.percent_bachelor,
        Cms.percent_white,
        Cms.percent_black,
        Cms.percent_american_indian,
        Cms.percent_asian,
        Cms.percent_hawaiian,
        Cms.percent_some_other,
        Cms.percent_two_or_more
    ).all()

    session.close()

    cms_data = []
    for state, state_name, facility_name, measure, score, poverty, veteran, married, bachelor, white, black, a_indian, asian, hawaiian, some_other, two_or_more in results:
        cms_dict = {}
        cms_dict["state"] = state
        cms_dict["state_name"] = state_name
        cms_dict["facility_name"] = facility_name
        cms_dict["measure"] = measure
        cms_dict["score"] = score
        cms_dict["poverty"] = poverty
        cms_dict["veteran"] = veteran
        cms_dict["married"] = married
        cms_dict["bachelor"] = bachelor
        cms_dict["white"] = white
        cms_dict["black"] = black
        cms_dict["a_indian"] = a_indian
        cms_dict["asian"] = asian
        cms_dict["hawaiian"] = hawaiian
        cms_dict["some_other"] = some_other
        cms_dict["two_or_more"] = two_or_more
        cms_data.append(cms_dict)

    return jsonify(cms_data)

#
# Summarize state mortality data and send back
#


@app.route("/mortalities/<state>")
def mortalities(state):
    # Create session (link) from Python to the DB
    session = Session(engine)

    """Return a list of a dicionary for mortalites by state"""
    # Query all for mortality
    query = session.query(Cms.measure_name, func.avg(Cms.score))

    # check for the all condition and filter if valid state passed
    if state != "all":
        query = query.filter(Cms.state == state)

    # group by measure name for uniqueness
    query = query.group_by(Cms.measure_name)

    # Get all the results
    results = query.all()

    session.close()

    cms_data = []
    for measure, score in results:
        cms_dict = {}
        cms_dict["measure"] = measure
        cms_dict["score"] = score
        cms_data.append(cms_dict)

    return jsonify(cms_data)

#
# Get a list of unique states
#


@app.route("/states")
def states():
    # Create session (link) from Python to the DB
    session = Session(engine)

    """Return a list of a dictionary for states"""
    results = session.query(Cms.state, Cms.state_name)\
        .group_by(Cms.state, Cms.state_name)\
        .order_by(Cms.state_name)\
        .all()

    session.close()

    state_data = []
    for state, state_name in results:
        state_dict = {}
        state_dict["state"] = state
        state_dict["state_name"] = state_name
        state_data.append(state_dict)

    return jsonify(state_data)

    #
# Get a list of unique measures
#


@app.route("/measures")
def measures():
    # Create session (link) from Python to the DB
    session = Session(engine)

    """Return a list of a dictionary for measures"""
    results = session.query(Cms.measure_name)\
        .group_by(Cms.measure_name)\
        .order_by(Cms.measure_name)\
        .all()

    session.close()

    measure_data = []
    for measure_name in results:
        measure_dict = {}
        measure_dict["measure"] = measure_name[0] 
        measure_data.append(measure_dict)


    return jsonify(measure_data)


@app.route("/racemortalities/<death>")
def racemortalities(death):
    # Create session (link) from Python to the DB
    session = Session(engine)

    """Return a list of a dicionary for mortalites by state"""
    # Query all for mortality
    query = session.query(func.avg(Cms.score), Cms.race_category)

    # check for the all condition and filter if valid state passed
    # death = "Death rate for COPD patients"
    # death = "Death rate for pneumonia patients"
    # death =  "Death rate for heart attack patients"
    # death = "Death rate for heart failure patients"
    query = query.filter(Cms.measure_name == death)
    query = query.group_by(Cms.state, Cms.county_name, Cms.measure_name, Cms.race_category)

    # Get all the results
    results = query.all()

    session.close()

    white_scores = []
    black_scores = []
    for score, race_category in results:
        if race_category == "W":
            white_scores.append(score)
        else: 
            black_scores.append(score)

    cms_data = {
        "measure": death,
        "white_scores": white_scores,
        "black_scores": black_scores,
    }
    return jsonify(cms_data)

if __name__ == '__main__':
    app.run(debug=True)
