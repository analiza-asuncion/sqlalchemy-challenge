# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import desc
from sqlalchemy import create_engine, inspect, func
from sqlalchemy.sql import text
from flask import Flask, jsonify
import datetime as dt
import pandas as pd
import numpy as np
engine = create_engine("sqlite:///Resources/hawaii.sqlite", echo=False)

# reflect an existing database into a new model
# Reflect Database into ORM class
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement



Measure = Base.classes.measurement
Station = Base.classes.station

app = Flask(__name__)

@app.route("/")
def welcome():
    return( 
        f"-----List All Routes API-----<br/>"
        f"Note: Paste the routes in the browsing after the default link<br/>"
        f"Available Routes Below:<br/>"
        f"<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"<br/>"
        f"/api/v1.0/stations<br/>"
        f"<br/>"
        f"/api/v1.0/tobs<br/>"
        f"<br/>"
        f"/api/v1.0/<start><br/>"
        f"Put the start date in 'YYYY-MM-DD' format<br/>"
        f"<br/>"
        f"/api/v1.0/<start>/<end><br/>"   
        f"Put the dates in 'YYYY-MM-DD/YYYY-MM-DD' format<br/>"
        )      

@app.route("/api/v1.0/precipitation")
def precipitation():
    session= Session(engine)
    results = session.query(Measure.date,Measure.prcp).all()
    all_date_prcp = []
    for date,prcp in results:
        measure_dict = {}
        measure_dict["date"] = date
        measure_dict["prcp"] = prcp
        all_date_prcp.append(measure_dict)
    session.close()
    return jsonify(all_date_prcp)

@app.route("/api/v1.0/stations")
def stations():
    session= Session(engine)
    stations = session.query(Station.station,Station.name).all()
    list_stations=[]
    for station in stations:
        station_dict = {}
        station_dict["station"] = station
        list_stations.append(station_dict)
    session.close()
    return jsonify(list_stations)

#Return a JSON list of temperature observations (TOBS) for the previous year.
@app.route("/api/v1.0/tobs")
def tobs():
    session= Session(engine)
    tobs_query = session.query(Measure.date, Measure.tobs, Measure.station).filter(Measure.date > '2016-08-22', Measure.date <'2017-08-24').filter(text("station = :value")).params(value = "USC00519281").all()
    tobs_list =[]
    for date, tobs, station in tobs_query:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        tobs_dict["station"] = station
        tobs_list.append(tobs_dict)
    session.close()
    return jsonify(tobs_list)

#Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start
@app.route("/api/v1.0/start")
def tstart():
    # last data point
    #Step 2: Get the year old date (Last year)
    # last data point
    session= Session(engine)
    
    Latest_date = session.query(func.max(Measure.date)).first()
    #print(latest_date)
    End_Date = Latest_date[0]
    print(End_Date)
    
    Struct = dt.date.today()
    End_Date_dateformat = Struct.replace(year=int(End_Date[:4]),month=int(End_Date[5:7]),day=int(End_Date[8:]))
    Last_date_year = End_Date_dateformat - dt.timedelta(days=365)    
    Start_Date = Last_date_year.strftime("%Y-%m-%d")
    
    
    results = session.query(func.min(Measure.tobs).label("min_tobs"),func.max(Measure.tobs).label("max_tobs"),func.avg(Measure.tobs).label("ave_tobs")).filter(Measurement.date >= Last_date_year).all()
    list = []
    print(f"Temperature Analysis for the dates based on the condition")
    for min_tobs,max_tobs, ave_tobs in results:
        stats_dict = {}
        stats_dict["min_tobs"] = min_tobs
        stats_dict["max_tobs"] = max_tobs
        stats_dict["ave_tobs"] = ave_tobs
        {"Minimum Temp":min_tobs,"Average Temp":ave_tobs,"Maximum Temp":max_tobs}
        list.append(stats_dict)
    session.close()
    return jsonify(list) 
#[(58.0, 87.0, 74.59058295964125)]


#When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.
@app.route("/api/v1.0/start_end")
def start_end():
    session= Session(engine)
    #Earliest date
    old_date=session.query(func.min(Measure.date)).all()
    #print(old_date)
    Beginning_date = old_date[0][0]

    Latest_date = session.query(func.max(Measure.date)).first()
    #print(latest_date)
    End_Date = Latest_date[0]
    print(End_Date)    
    
    Struct = dt.date.today()
    End_Date_dateformat = Struct.replace(year=int(End_Date[:4]),month=int(End_Date[5:7]),day=int(End_Date[8:]))
    Last_date_year = End_Date_dateformat - dt.timedelta(days=365)    
    Start_Date = Last_date_year.strftime("%Y-%m-%d")
    
    results = session.query(func.min(Measure.tobs).label("min_tobs"),func.max(Measure.tobs)\
                     .label("max_tobs"),func.avg(Measure.tobs).label("ave_tobs"))\
                     .filter(Measurement.date >= Beginning_date, Measurement.date <=Last_date_year).all()
    list = []
    print(f"Temperature Analysis for the dates based on the condition")
     
    for min_tobs,max_tobs, ave_tobs in results:
        last_dict = {}
        last_dict["min_tobs"] = min_tobs
        last_dict["max_tobs"] = max_tobs
        last_dict["ave_tobs"] = ave_tobs
        {"Minimum Temp":min_tobs,"Average Temp":ave_tobs,"Maximum Temp":max_tobs}
        list.append(last_dict)
    session.close()
    return jsonify(list) 



if __name__ == "__main__":
    app.run(debug=True)

