# Import the dependencies
from flask import Flask, jsonify
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import pandas as pd
import numpy as np


#################################################
# Database Setup
#################################################
# Create engine to connect to the SQLite database
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Station = Base.classes.station
Measurement = Base.classes.measurement

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
# Initialize Flask
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Welcome to the Hawaii Climate API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start (replace 'start' with the start date)<br/>"
        f"/api/v1.0/start/end (replace 'start' and 'end' with the start and end dates)<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return the last 12 months of precipitation data."""
    # Query for the last 12 months of precipitation data
    most_recent_date = session.query(func.max(Measurement.date)).scalar()
    one_year_ago = (pd.to_datetime(most_recent_date) - pd.DateOffset(years=1)).strftime('%Y-%m-%d')
    
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= one_year_ago).all()

    # Create a dictionary from the row data then return it as JSON
    precipitation_data = {date: prcp for date, prcp in results}
    
    return jsonify(precipitation_data)


@app.route("/api/v1.0/stations")
def stations():
    """Return a list of weather stations."""
    # Query to get the list of stations
    results = session.query(Station.station, Station.name).all()
    stations_list = [{"station": station, "name": name} for station, name in results]
    
    return jsonify(stations_list)


@app.route("/api/v1.0/tobs")
def tobs():
    """Return the temperature observations (tobs) for the last 12 months."""
    # Get the most active station
    active_station_id = session.query(Measurement.station, func.count(Measurement.station)).\
        group_by(Measurement.station).\
        order_by(func.count(Measurement.station).desc()).first()[0]

    # Get the most recent date for this station
    most_recent_date_station = session.query(Measurement.date).\
        filter(Measurement.station == active_station_id).\
        order_by(Measurement.date.desc()).first()[0]

    # Calculate the date one year ago
    one_year_ago = (pd.to_datetime(most_recent_date_station) - pd.DateOffset(years=1)).strftime('%Y-%m-%d')

    # Query the temperature observations for the last 12 months
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == active_station_id).\
        filter(Measurement.date >= one_year_ago).\
        order_by(Measurement.date).all()

    # Create a dictionary from the row data and return it as JSON
    tobs_data = {date: tobs for date, tobs in results}
    
    return jsonify(tobs_data)


# Dynamic Route for temperatures from the start date to the end of the dataset
@app.route("/api/v1.0/<start>")
def start(start):
    """Return min, max, and average temperatures from the start date to the end of the dataset."""
    # Query min, max, and avg temperatures from the start date to the end of the dataset
    results = session.query(func.min(Measurement.tobs), 
                            func.max(Measurement.tobs), 
                            func.avg(Measurement.tobs)).\
              filter(Measurement.date >= start).all()

    # Handle case where no results are found
    if not results or results[0][0] is None:
        return jsonify({"error": f"No data found for start date {start}."}), 404

    # Convert query results into a list
    temp_stats = list(np.ravel(results))

    return jsonify({
        "Start Date": start,
        "Temperature Stats": {
            "Min Temp": temp_stats[0],
            "Max Temp": temp_stats[1],
            "Avg Temp": temp_stats[2]
        }
    })


@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    """Return min, max, and average temperatures from the start date to the end date."""
    # Query min, max, and avg temperatures from the start date to the end date
    results = session.query(func.min(Measurement.tobs), 
                            func.max(Measurement.tobs), 
                            func.avg(Measurement.tobs)).\
              filter(Measurement.date >= start).\
              filter(Measurement.date <= end).all()

    # Handle case where no results are found
    if not results or results[0][0] is None:
        return jsonify({"error": f"No data found between {start} and {end}."}), 404

    # Convert query results into a list
    temp_stats = list(np.ravel(results))

    return jsonify({
        "Start Date": start,
        "End Date": end,
        "Temperature Stats": {
            "Min Temp": temp_stats[0],
            "Max Temp": temp_stats[1],
            "Avg Temp": temp_stats[2]
        }
    })


if __name__ == "__main__":
    app.run(debug=True)
