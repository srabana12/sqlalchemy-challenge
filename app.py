# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine,desc,func
import datetime as dt
import pandas as pd
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)


# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our (link) from Python to the DB


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
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    most_recent_date_s = session.query(Measurement.date).order_by(desc(Measurement.date)).first()[0]
    most_recent_date = pd.to_datetime(most_recent_date_s)

    # Calculate the date one year from the last date in data set.
    one_year_ago_date = most_recent_date - pd.DateOffset(years=1)
    one_year_ago_date_str = one_year_ago_date.strftime('%Y-%m-%d')

    # query the last 12 months of precipitation data
    prcp_results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= one_year_ago_date_str).all()

    # convert the query results to a dictionary using date as the key and prcp as the value
    prcp_dict = {}
    for result in prcp_results:
        prcp_dict[result.date] = result.prcp

    # close the session
    session.close()

    # return the JSON representation of the dictionary
    return jsonify(prcp_dict)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    """Return a list of stations from the dataset."""
    results = session.query(Station.station).all()
    session.close()

    # Convert list of tuples into normal list
    stations = list(np.ravel(results))

    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    # Query the most active station
    most_active_station = session.query(Measurement.station).\
        group_by(Measurement.station).\
        order_by(func.count().desc()).\
        first()[0]
    
    # Calculate the date 1 year ago from the last data point in the database
    last_date = session.query(Measurement.date).\
        order_by(Measurement.date.desc()).\
        first()[0]
    
    one_year_ago_date = dt.datetime.strptime(last_date, '%Y-%m-%d') - dt.timedelta(days=365)
    
    # Query the temperature observations of the most active station for the last year of data
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == most_active_station).\
        filter(Measurement.date >= one_year_ago_date).\
        all()
    session.close()
    # Create a list of temperature observations
    temps = [result[0] for result in results]
    
    # Return the JSON representation of the list
    return jsonify(temps)

@app.route("/api/v1.0/<start>")
def temperature_range_start(start):
    session = Session(engine)

    # query the minimum, average, and maximum temperature data for all dates greater than or equal to the start date
    temp_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).all()

    # close the session
    session.close()

    # create a list of dictionaries to store the temperature data
    temp_data = []
    for result in temp_results:
        temp_dict = {}
        temp_dict['TMIN'] = result[0]
        temp_dict['TAVG'] = result[1]
        temp_dict['TMAX'] = result[2]
        temp_data.append(temp_dict)

    # return the JSON representation of the list of dictionaries
    return jsonify(temp_data)

@app.route("/api/v1.0/<start>/<end>")
def temperature_range_start_end(start, end):
    session = Session(engine)

    # query the minimum, average, and maximum temperature data for all dates between the start and end dates (inclusive)
    temp_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    # close the session
    session.close()

    # create a list of dictionaries to store the temperature data
    temp_data = []
    for result in temp_results:
        temp_dict = {}
        temp_dict['TMIN'] = result[0]
        temp_dict['TAVG'] = result[1]
        temp_dict['TMAX'] = result[2]
        temp_data.append(temp_dict)

    # return the JSON representation of the list of dictionaries
    return jsonify(temp_data)


if __name__ == '__main__':
    app.run(debug=True)
