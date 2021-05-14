#import dependencies
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

#create database engine
engine = create_engine("sqlite:///hawaii.sqlite")
#reflect an existing database into new model
base = automap_base()
#reflect the tables
base.prepare(engine, reflect=True)
#generate keys
base.classes.keys()

Measurement = base.classes.measurement
Station = base.classes.station

session = Session(engine)

#app creation
app = Flask(__name__)

final_date = (session.query(Measurement.date).order_by(Measuerment.date.desc()).first())


@app.route("/")
def home():
    return (f"Hawaii Weather Station and Percipitation API, Surfs up!"
            f"-------------------------------------------------------"
            f"Available API routes listed below"
            f"/api/v1.0/precipitation"
            f"/api/v1.0/stations"
            f"/api/v1.0/tobs"
            f"/api/v1.0/<startdate>"
            f"/api/v1.0/<startdate>/<enddate>")

@app.route("/api/v1.0/precipitation")
def precip():
        results = (session.query(Measurement.date, Measurement.prcp, Measurement.station)
                            .filter(Measurement.date > last_year)
        )

