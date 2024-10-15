# sqlalchemy-challenge
## Table of contents

* [Description](#Description)
* [Database Setup and Exploration](#Database-Setup-and-Exploration)
* [Precipitation Data Analysis](#Precipitation-Data-Analysis)
* [Design Your Climate App](#Design-Your-Climate-App)
* [app.py Image](#app-py-Image)
* [Questions](#Questions)
* [References](#References)

## Description

I've decided to treat myself to a long holiday vacation in Honolulu, Hawaii. To help with my trip planning, I decide to do a climate analysis about the area. 

## Database Setup and Exploration

* Using SQLAlchemy to connect to the SQLite database (hawaii.sqlite) containing two tables: station and measurement.
* The automap_base() function reflects the database schema, providing an easy access to the tables via ORM models.
* When inspecting the database schema it showed the column names and data types in both tables.


## Precipitation Data Analysis
* The most recent date in the measurement table is found to be '2017-08-23'.
* Using the most recent date, calculateing the date one year prior and retrieves precipitation data for the last 12 months.
* The precipitation data is plotted using matplotlib. The plot reveals the range of precipitation values over the 12-month period.

## Design Your Climate App

The app.py script is built using Flask, to create an API or web service that allows users to query and retrieve climate data such as temperature and precipitation. The goal of this application is to provide easy access to the results of the data exploration and visualizations performed in the climate analysis, making the data accessible via web routes.

## app.py Image

![data modeling](/Resources/app.py-routes.png)
![data modeling](/Resources/app.py-routes-explorer.gif)

## Questions

In case of any additional questions please visit my GitHub link: [Feda2020](https://github.com/Feda2020) 

## References
 
 * Flask (https://flask.palletsprojects.com/en/1.1.x/)
 * Flask-Gothub (https://github.com/pallets/flask)
 * SQLAlchemy (https://docs.sqlalchemy.org/en/20/)