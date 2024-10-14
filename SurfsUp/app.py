# Import the dependencies.
from flask import Flask, jsonify
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import pandas as pd


#################################################
# Database Setup
#################################################
# Create engine to connect to the SQLite database
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

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
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():

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
    # Query to get the list of stations
    results = session.query(Station.station, Station.name).all()
    stations_list = [{"station": station, "name": name} for station, name in results]
    
    return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def tobs():
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

if __name__ == "__main__":
    app.run(debug=True)