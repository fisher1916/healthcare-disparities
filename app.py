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
Fips = Base.classes.lat_lon_fips

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    return render_template("index.html")


#
# Summarize state mortality data and send back
#

@app.route("/mortalities/<state>")
def mortalities(state):

    # Get the measure scores
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

    # Get the average race percent
    # Create session (link) from Python to the DB
    session = Session(engine)

    """Return a list of a dicionary for race by state"""
    # Query all for races
    query = session.query(func.avg(Cms.percent_white),
                          func.avg(Cms.percent_black))

    # check for the all condition and filter if valid state passed
    if state != "all":
        query = query.filter(Cms.state == state)

    # print(query.statement.compile())

    # Get all the results
    results = query.first()

    session.close()

    demo_data = []

    demo_dict = {}
    demo_dict["name"] = "White"
    demo_dict["percent"] = results[0]
    demo_data.append(demo_dict)

    demo_dict = {}
    demo_dict["name"] = "Black"
    demo_dict["percent"] = results[1]
    demo_data.append(demo_dict)

    # Get the average urban / rural percent
    # Create session (link) from Python to the DB
    session = Session(engine)

    """Return a list of a dicionary for population by state"""
    # Query all for population
    query = session.query(func.sum(Cms.total_population))

    # Grab rural numbers only less than or equal to 50000
    query = query.filter(Cms.total_population <= 50000)

    # check for the all condition and filter if valid state passed
    if state != "all":
        query = query.filter(Cms.state == state)

    # print(query.statement.compile())

    # Get all the results
    results = query.first()

    session.close()

    rural_total = 0
    if not results[0] is None:
        rural_total = int(results[0])

    # Get the average urban / rural percent
    # Create session (link) from Python to the DB
    session = Session(engine)

    """Return a list of a dicionary for population by state"""
    # Query all for population
    query = session.query(func.sum(Cms.total_population))

    # Grab urban numbers only greater than 50000
    query = query.filter(Cms.total_population > 50000)

    # check for the all condition and filter if valid state passed
    if state != "all":
        query = query.filter(Cms.state == state)

    # print(query.statement.compile())

    # Get all the results
    results = query.first()

    session.close()

    urban_total = 0
    if not results[0] is None:
        urban_total = int(results[0])

    total_population = rural_total + urban_total

    if total_population == 0:
        total_population = 1

    demo_dict = {}
    demo_dict["name"] = "Rural"
    demo_dict["percent"] = (rural_total/total_population) * 100
    demo_data.append(demo_dict)

    demo_dict = {}
    demo_dict["name"] = "Urban"
    demo_dict["percent"] = (urban_total/total_population) * 100
    demo_data.append(demo_dict)

    return_data = {}
    return_data["measures"] = cms_data
    return_data["demo"] = demo_data

    return jsonify(return_data)

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

#
# Get race data by mortality (death) category
#


@app.route("/racemortalities/<death>")
def racemortalities(death):
    # Create session (link) from Python to the DB
    session = Session(engine)

    """Return a list of a dicionary for mortalites by state"""
    # Query all for mortality
    query = session.query(func.avg(Cms.score), Cms.race_category)

    # check for the all condition and filter if valid state passed
    # death = "Death rate for pneumonia patients"
    # death =  "Death rate for heart attack patients"
    # death = "Death rate for heart failure patients"
    query = query.filter(Cms.measure_name == death)
    query = query.group_by(Cms.state, Cms.county_name,
                           Cms.measure_name, Cms.race_category)

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

#
# Get urban/rural data by mortality (death) category
#


@app.route("/urbanruralmortalities/<death>")
def urbanruralmortalities(death):
    # Create session (link) from Python to the DB
    session = Session(engine)

    """Return a list of a dicionary for mortalites by state"""
    # Query all for mortality
    query = session.query(func.avg(Cms.score), Cms.urban_rural_category)

    # check for the all condition and filter if valid state passed
    query = query.filter(Cms.measure_name == death)
    query = query.group_by(Cms.state, Cms.county_name,
                           Cms.measure_name, Cms.urban_rural_category)

    # Get all the results
    results = query.all()

    session.close()

    urban_scores = []
    rural_scores = []
    for score, urban_rural_category in results:
        if urban_rural_category == "URBAN":
            urban_scores.append(score)
        else:
            rural_scores.append(score)

    cms_data = {
        "measure": death,
        "urban_scores": urban_scores,
        "rural_scores": rural_scores,
    }
    return jsonify(cms_data)


#
# Get all county data by mortality (death) category
#


@app.route("/getallmortalities")
def getallmortalities():
    # Create session (link) from Python to the DB
    session = Session(engine)

    """Return a list of a dicionary for mortalites by state"""
    # Query all for mortality
    query = session.query(
        Cms.state,
        Cms.county_name,
        Cms.measure_name,
        Cms.total_population,
        Cms.race_category,
        Cms.urban_rural_category,
        Fips.lat,
        Fips.long,
        func.avg(Cms.score)
    )

    #death = "Death rate for COPD patients"

    # check for the all condition and filter if valid state passed
    query = query.filter(
        #    Cms.measure_name == death,
        Cms.state_code == Fips.state_code,
        Cms.county_code == Fips.county_code,
    )
    query = query.group_by(
        Cms.state,
        Cms.county_name,
        Cms.measure_name,
        Cms.total_population,
        Cms.race_category,
        Cms.urban_rural_category,
        Fips.lat,
        Fips.long
    )

    # print(query.statement.compile())

    # Get all the results
    results = query.all()

    session.close()

    counties = []
    for state, county, measure_name, population, race, urban_rural, lat, lng, score in results:
        county_dict = {}
        county_dict["coordinates"] = [lat, lng]

        detail_dict = {}
        detail_dict["county"] = county
        detail_dict["state"] = state
        detail_dict["population"] = population
        detail_dict["race"] = race
        detail_dict["area"] = urban_rural
        detail_dict["score"] = score

        county_dict[measure_name] = detail_dict

        counties.append(county_dict)

    return jsonify(counties)


# main program
if __name__ == '__main__':
    app.run(debug=True)
