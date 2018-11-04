# `/api/v1.0/precipitation`

  # Query for the dates and temperature observations from the last year.

  # Convert the query results to a Dictionary using `date` as the key and `tobs` as the value.

  # Return the JSON representation of your dictionary.

# `/api/v1.0/stations`

  # Return a JSON list of stations from the dataset.

# `/api/v1.0/tobs`

  # Return a JSON list of Temperature Observations (tobs) for the previous year.

# `/api/v1.0/<start>` and `/api/v1.0/<start>/<end>`

  # Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
# When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.

# When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.
  

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

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
climateapp = Flask(__name__)


#################################################
# Flask Routes
#################################################

@climateapp.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )


@climateapp.route("/api/v1.0/precipitation")
def precipitation():
    """Return a list of all passenger names"""
    # Query all precipitation data
    results = session.query(Measurement.date, Measurement.prcp).\
                        filter(Measurement.date > '2016-08-23').\
                        order_by(Measurement.date).all()

  
    all_prcp = []
    for prcp_data in results:
        prcp_dict = {}
        prcp_dict["Date"] = prcp_data.date
        prcp_dict["Precipitation"] = prcp_data.prcp
        all_prcp.append(prcp_data_dict)
    return jsonify(all_prcp)


@climateapp.route("/api/v1.0/stations")
def stations():
    """Return a list of passenger data including the name, age, and sex of each passenger"""
    # Query all the stations
    results = session.query(Station.station).all()

    # Create a list for the stations
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)


@climateapp.route("/api/v1.0/tobs")
def tobs():
    # Query all measurements and for the given date. 
    results = session.query(Measurement.station, Measurement.date, Measurement.tobs).\
                    group_by(Measurement.date).\
                    filter(Measurement.date > '2016-08-23').\
                    order_by(Measurement.station).all()
    
    # create a dictionary for the tobs data
    all_tobs = []
    for tobs_data in results:
        tobs_data_dict = {}
        tobs_dict["Station"] = tobs_data.station
        tobs_dict["Date"] = tobs_data.date
        tobs_dict["Temperature"] = tobs_data.tobs
        all_tobs.append(tobs_data_dict)
    
    return jsonify(all_tobs)


@climateapp.route("/api/v1.0/<start>")

def start_stats(start):
    # Query the measurements starting from the given date. 
    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
    filter(Measurement.date >= start).all()
    
    # Create a dictionary from the row data and append to a list of for the temperature data.
    temp_stats = []
    
    for Tmin, Tmax, Tavg in results:
        temp_dict = {}
        temp_dict["Minimum Temp"] = Tmin
        temp_dict["Maximum Temp"] = Tmax
        temp_dict["Average Temp"] = Tavg
        temp_stats.append(temp_dict)
    
    return jsonify(temp_stats)
                  
@climateapp.route("/api/v1.0/<start>/<end>")
def calc_stats(start=None, end=None):
    
    # Query all the stations and for the given range of dates. 
    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
    filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    # Create a dictionary from the row data and append to a list of for the temperature data.
    begin_end_stats = []
    
    for Tmin, Tmax, Tavg in results:
        begin_end_dict = {}
        begin_end_dict["Minimum Temp"] = Tmin
        begin_end_dict["Maximum Temp"] = Tmax
        begin_end_dict["Average Temp"] = Tavg
        begin_end_dict['start']=start
        begin_end_dict['end']=end
        begin_end_stats.append(begin_end_dict)
    
    return jsonify(begin_end_stats)


if __name__ == '__main__':
    climateapp.run(debug=True)
