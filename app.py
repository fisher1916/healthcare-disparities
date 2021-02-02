import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify, render_template

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///ETL/cmsdb.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
cms = Base.classes.cms

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
    return render_template("index.html")


@app.route("/mortality")
def ():
    # Create session (link) from Python to the DB
    session = Session(engine)

    """Return a list of a dicionary for mortality"""
    # Query all for mortality
    results = session.query().all()
    
    session.close()

    return jsonify(mort_dict)

if __name__ == '__main__':
    app.run(debug=True)

