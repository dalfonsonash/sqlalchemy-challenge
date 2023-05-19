# Import the dependencies.
import sqlalchemy
from flask import Flask, jsonify
import datetime as dt
import numpy as np
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect


#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

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
# Define the index route
@app.route("/")
def index():
    return """
        Welcome to the Climate API!<br/>
        Available Routes:<br/>
        /api/v1.0/precipitation<br/>
        /api/v1.0/stations<br/>
        /api/v1.0/tobs<br/>
        /api/v1.0/<start><br/>
        /api/v1.0/<start>/<end>
    """

# Define the precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    session=Session(engine)
    # Calculate the date one year ago from the last data point
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    one_year_ago = dt.date.fromisoformat(last_date[0]) - dt.timedelta(days=365)
    
    # Query the precipitation data for the last 12 months
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= one_year_ago).all()
    
    # Convert the query results to a dictionary with date as the key and prcp as the value
    precipitation_data = {date: prcp for date, prcp in results}
    
    session.close()
    # Return the JSON representation of the dictionary
    return jsonify(precipitation_data)

# Define the stations route
@app.route("/api/v1.0/stations")
def stations():
    session=Session(engine)
    # Query the list of stations
    results = session.query(Station.station).all()
    
    # Convert the query results to a list
    station_list = [station for station, in results]
    
    
    session.close()
    # Return the JSON representation of the list
    return jsonify(station_list)
most_active_station = "USC00519281"
# Define the tobs route
@app.route("/api/v1.0/tobs")
def tobs():
    session=Session(engine)
    # Calculate the date one year ago from the last data point
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    one_year_ago = dt.date.fromisoformat(last_date[0]) - dt.timedelta(days=365)
    
    # Query the temperature observations for the most active station in the last 12 months
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= one_year_ago).\
        filter(Measurement.station == most_active_station).all()
    
    # Convert the query results to a list of dictionaries
    tobs_list = []
    for date, tobs in results:
        tobs_list.append({"date": date, "tobs": tobs})
    
    session.close()
    # Return the JSON representation of the list
    return jsonify(tobs_list)

# Define the start and start/end date routes
@app.route("/api/v1.0/start_date/<start>")
def start_date(start):
    try:
        start_date = dt.datetime.strptime(start, "%Y-%m-%d").date()
    except ValueError:
        return jsonify({"error": "Invalid date format. Please use YYYY-MM-DD."}), 400

    session = Session(engine)
    
    # Perform the necessary calculations using the specified start date
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
              filter(Measurement.date >= start).all()
    
    session.close()
    
    # Check if any data is available for the specified start date
    if results:
        # Create a dictionary with the calculated values
        temp_data = {
            "TMIN": results[0][0],
            "TAVG": results[0][1],
            "TMAX": results[0][2]
        }
        
        return jsonify(temp_data)
    
    # If no data is available, return an error message
    return jsonify({"error": f"No temperature data found for the specified start date '{start}'"}), 404


@app.route("/api/v1.0/start_end_date/<start>/<end>")
def start_end_date(start, end):
    try:
        start_date = dt.datetime.strptime(start, "%Y-%m-%d").date()
        end_date = dt.datetime.strptime(end, "%Y-%m-%d").date()
    except ValueError:
        return jsonify({"error": "Invalid date format. Please use YYYY-MM-DD."}), 400
    
    session = Session(engine)
    
    # Perform the necessary calculations using the specified start and end dates
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
              filter(Measurement.date >= start, Measurement.date <= end).all()
    
    session.close()
    
    # Check if any data is available for the specified start and end dates
    if results:
        # Create a dictionary with the calculated values
        temp_data = {
            "TMIN": results[0][0],
            "TAVG": results[0][1],
            "TMAX": results[0][2]
        }
        
        return jsonify(temp_data)
    
    # If no data is available, return an error message
    return jsonify({"error": f"No temperature data found for the specified start date '{start}' and end date '{end}'"}), 404

# Run the server
if __name__ == "__main__":
    app.run(debug=True)