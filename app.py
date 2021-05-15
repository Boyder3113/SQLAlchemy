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
Base = automap_base()
#reflect the tables
Base.prepare(engine, reflect=True)

measurement = Base.classes.measurement
station = Base.classes.station

session = Session(engine)

#app creation
app = Flask(__name__)

recent_date = (session.query(measurement.date).order_by(measurement.date.desc()).first())
recent_date_ravel = list(np.ravel(recent_date))[0]

last_date = dt.datetime.strftime(recent_date_ravel, '%Y-%m-%d')
year_int = int(dt.datetime.strftime(last_date, '%Y'))
month_int = int(dt.datetime.strftime(last_date, '%m'))
day_int = int(dt.datetime.strftime(last_date, '%d'))

last_year = dt.date(year_int, month_int, day_int) - dt.timedelta(days=365)
last_year_int = dt.datetime.strftime(last_year, '%Y-%m-%d')


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
        results = (session.query(measurement.date, measurement.prcp, measurement.station)
                            .filter(measurement.date >= last_year)
                            .order_by(measurement.date).all())
        
        rainData = []

        for r in results:
                rainDict = {result.date: result.prcp, "Station": result.station}
                rainData.append(rainDict)
        
        return jsonify(rainData)

@app.route("/api/v1.0/stations")
def stations():
        station_names = session.query(Station.name).all()
        stations = list(np.ravel(station_names))
        return jsonify(all_stations)


@app.route("/api/v1.0/tobs")
def tobs():
       
        temp = (session.query(measurement.date, measurement.tobs, measurement.station)
                .filter(measurement.date >= last_year)
                .orber_by(measurement.date) .all())
        
        tobsData = []

        for t in temp:
                tobsDict = {temp.date: temp.tobs, "Station":temp.station}
                tobsData.append(tempDict)

        return jsonify(tobsData)

@app.route("/api/v1.0/<startdate>")
def startDateSearch(startdate):
        sel = [measurement.date, func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)]

        dateResults = (session.query(*sel).filter(func.strftime("%Y-%m-%d",measurement.date)>= startdate).group_by(measurement.date).all())

        date_list = []

        for day in dateResults:
                date_dict = {}
                date_dict["Date"] = dateResults[0]
                date_dict["Low Temp"] = dateResults[1]
                date_dict["Average Temp"] = dateResults[2]
                date_dict["High Temp"] = dateResults[3]
                date_list.append(date_dict)
        return jsonify(date_list)

@app.route("/api/v1.0/<startdate>/<enddate>")
def datesearch(startdate, enddate):
        sel = [measurement.date, func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)]

        dateSearchResults = (session.query(*sel).filter(func.strftime("%Y-%m-%d",measurement.date)>= startdate).filter(func.strftime("%Y-%m-%d",measurement.date) <= enddate).group_by(measurement.date).all())

        dateSearch_list = []

        for day in dateSearchResults:
                dateSearch_dict = {}
                dateSearch_dict["Date"] = dateResults[0]
                dateSearch_dict["Low Temp"] = dateResults[1]
                dateSearch_dict["Average Temp"] = dateResults[2]
                dateSearch_dict["High Temp"] = dateResults[3]
                dateSearch_list.append(date_dict)
        return jsonify(date_list)

        
if __name__ == '__main__':
    app.run(debug=True)
