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
    return render_template("index.html")


@app.route("/mortality")
def mortality():
    # Create session (link) from Python to the DB
    session = Session(engine)

    """Return a list of a dicionary for mortality"""
    # Query all for mortality
    results = session.query(
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
    for name, measure, score, poverty, veteran, married, bachelor, white, black, a_indian, asian, hawaiian, some_other,two_or_more in results:
        cms_dict = {}
        cms_dict["name"] = name
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

    print(len(cms_data))
    return jsonify(cms_data)

if __name__ == '__main__':
    app.run(debug=True)

