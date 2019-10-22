import numpy as np

import datetime as dt 

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite",connect_args={'check_same_thread': False})

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

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
        f"<center> <h2> Available Routes </h2> </center>"
        f"<hr/>"
        f"<b> <ins> 1)  Percipitation Data </ins> </b> <br/>"
        f"<a href=http://127.0.0.1:5000/api/v1.0/precipitation>/api/v1.0/precipitation </a> <br/>"
        f" <br/>"
        
        f"<b> <ins> 2)  Stations Data </ins> </b> <br/>"
        f"<a href=http://127.0.0.1:5000/api/v1.0/stations>/api/v1.0/stations </a> <br/>"
        f" <br/>"
        
        f"<b> <ins> 3) Temperature Observations (tobs) for the Previous Year: </ins> </b> <br/>"
        f"<a href=http://127.0.0.1:5000/api/v1.0/tobs> /api/v1.0/tobs </a> <br/>"
        f" <br/>"
        
        f"<b> <ins> 4) Temperature Details for all dates greater than and equal to the Start Date </ins> </b> "
        f" (Temperature Details --> Maximum, Minimum & Average Temperature) <br/>"
        f" (/api/v1.0/Start Date) <br/><br/>"
        f"<a href=http://127.0.0.1:5000/api/v1.0/2017-01-01> /api/v1.0/2017-01-01 </a> <br/>"
        f"<a href=http://127.0.0.1:5000/api/v1.0/2016-01-01> /api/v1.0/2016-01-01 </a> <br/>"
        f"<a href=http://127.0.0.1:5000/api/v1.0/2015-01-01> /api/v1.0/2015-01-01 </a> <br/>"
        f"<a href=http://127.0.0.1:5000/api/v1.0/2014-01-01> /api/v1.0/2014-01-01 </a> <br/>"
        f"<a href=http://127.0.0.1:5000/api/v1.0/2013-01-01> /api/v1.0/2013-01-01 </a> <br/>"
        f" <br/>"
        
        
        f"<b> <ins> 5) Temperature Details for dates between the Start and End Date inclusive </ins> </b> "
        f" (Temperature Details --> Maximum, Minimum & Average Temperature) <br/>"
        f" (/api/v1.0/Start Date/End Date) <br/><br/>"
        f"<a href=http://127.0.0.1:5000/api/v1.0/2017-01-01/2017-01-15> /api/v1.0/2017-01-01/2017-01-15 </a><br/>"
        f"<a href=http://127.0.0.1:5000/api/v1.0/2016-01-01/2016-01-15> /api/v1.0/2016-01-01/2016-01-15 </a><br/>"
        f"<a href=http://127.0.0.1:5000/api/v1.0/2015-01-01/2015-01-15> /api/v1.0/2015-01-01/2015-01-15 </a><br/>"
        f"<a href=http://127.0.0.1:5000/api/v1.0/2014-01-01/2014-01-15> /api/v1.0/2014-01-01/2014-01-15 </a><br/>"
        f"<a href=http://127.0.0.1:5000/api/v1.0/2013-01-01/2013-01-15> /api/v1.0/2013-01-01/2013-01-15 </a><br/>"
        f" <br/>"
        
        f"<b> Note : The above are just the Sample Start & End Dates."
        f" We can even modify the Start & End dates to retrieve the Temperature Details for the 4th and 5th Routes.</b>"
        f"<hr/>"
        
    )


@app.route("/api/v1.0/precipitation")
def precipitation():

    LastDate = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    LastDate= dt.datetime.strptime(LastDate,"%Y-%m-%d")
    FirstDate = LastDate - dt.timedelta(days = 365)
    
    Precipitation_Data = session.query(Measurement.date,Measurement.prcp).\
                         filter(Measurement.date > FirstDate).\
                         order_by(Measurement.date).all()


    Precipitation_Data = dict(Precipitation_Data)

    return jsonify({'Precipitation Data':Precipitation_Data})

@app.route("/api/v1.0/stations")
def stations():

    # Query all Station
    Stations_Data = session.query(Station).all()

    # Create a dictionary from the Stations_Data and append to a list of Stations_Data_List
    Stations_Data_List = []
    for s in Stations_Data:
        Stations_dict = {}
        Stations_dict["Station"] = s.station
        Stations_dict["Station Name"] = s.name
        Stations_dict["Latitude"] = s.latitude
        Stations_dict["Longitude"] = s.longitude
        Stations_dict["Elevation"] = s.elevation
        Stations_Data_List.append(Stations_dict)

    return jsonify({'Station Data' : Stations_Data_List})

@app.route("/api/v1.0/tobs")
def tobs():
    
    LastDate = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    LastDate= dt.datetime.strptime(LastDate,"%Y-%m-%d")
    FirstDate = LastDate - dt.timedelta(days = 365)
    
    Temp_Observed_Data = session.query(Measurement.tobs, Measurement.date, Measurement.station).\
                         filter(Measurement.date > FirstDate).\
                         order_by(Measurement.date).all()

   # Create a dictionary from the Temp_Observed_Data and append to a list of Temp_Observed_Data_List
    Temp_Observed_Data_List = []
    for tob in Temp_Observed_Data:
        Temp_Observed_dict = {}
        Temp_Observed_dict["Station"] = tob.station
        Temp_Observed_dict["Date"] = tob.date
        Temp_Observed_dict["Temperature Observed"] = tob.tobs
        Temp_Observed_Data_List.append(Temp_Observed_dict)

    return jsonify({'Temperature Observations (tobs) data for the previous year' :Temp_Observed_Data_List})

@app.route("/api/v1.0/<start>")
def Temp_Data_By_Start(start=None):

    Temp_Data_ByStart = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs),func.max(Measurement.tobs)).\
                       filter(Measurement.date >= start).all()


    Temp_Data_ByStart_List = []
    for TMIN, TAVG, TMAX in Temp_Data_ByStart:
            Temp_Data_ByStart_dict = {}
            Temp_Data_ByStart_dict["Min Temp"] = TMIN
            Temp_Data_ByStart_dict["Max Temp"] = TAVG
            Temp_Data_ByStart_dict["Avg Temp"] = TMAX
            Temp_Data_ByStart_List.append(Temp_Data_ByStart_dict)

    return jsonify ({f"Minimum, Maximum & Average Temperature Details for all dates greater than and equal to {start}":Temp_Data_ByStart_List})

@app.route("/api/v1.0/<start>/<end>")
def Temp_Data_By_Start_End(start=None,end=None):

    Temp_Data_ByStartEnd = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs),func.max(Measurement.tobs)).\
                       filter(Measurement.date >= start,Measurement.date <= end).all()


    Temp_Data_ByStartEnd_List = []
    for TMIN, TAVG, TMAX in Temp_Data_ByStartEnd:
            Temp_Data_ByStartEnd_dict = {}
            Temp_Data_ByStartEnd_dict["Min Temp"] = TMIN
            Temp_Data_ByStartEnd_dict["Max Temp"] = TAVG
            Temp_Data_ByStartEnd_dict["Avg Temp"] = TMAX
            Temp_Data_ByStartEnd_List.append(Temp_Data_ByStartEnd_dict)

    return jsonify ({f" Minimum, Maximum & Average Temperature Details for dates between {start} and {end} ":Temp_Data_ByStartEnd_List})


if __name__ == '__main__':
    app.run(debug=True)