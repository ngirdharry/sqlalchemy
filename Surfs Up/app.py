#!/usr/bin/env python
# coding: utf-8

# In[127]:


#import dependencies 

import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func,inspect, distinct
import datetime as dt

from flask import Flask, jsonify


# In[128]:


#Database Set-up 
engine = create_engine("sqlite:///Resources/hawaii.sqlite")


# In[129]:


#Reflect database 
Base = automap_base()


# In[130]:


#Reflect tables 
Base.prepare(engine, reflect=True)


# In[131]:


# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station


# In[132]:


#Part 1: Flask Set-up & Start at the Homepage. 
app = Flask(__name__)


# In[133]:


#Part 1: List All available routes 
@app.route("/")
def home(): 
    routes = (
        "/api/v1.0/precipitation<br>"
        "/api/v1.0/stations<br>"
        "/api/v1.0/tobs<br>"
        "/api/v1.0/&lt;start&gt;/&lt;end&gt;<br>")
    return routes


# In[95]:


#Part 2: Precipitation route. Convert the query results from your precipitation analysis (i.e. retrieve only the 
#last 12 months of data) to a dictionary using date as the key and prcp as the value


@app.route("/api/v1.0/precipitation")
def precipitation():
    print("Server requested climate app precipitation page...")

    #Create session from py to database and Query dataes/precipitation  
    session = Session(engine)
    prcp_data = session.query(Measurement.date, Measurement.prcp).all()

    # close session
    session.close()

    # Query results to dictionary with date as the key and prcp as value.
    prcp_dict = {} 
    for date, prcp in prcp_data:
        prcp_dict[date] = prcp
    
    # Return a JSON list from the dataset.
    return jsonify(prcp_dict)


# In[134]:


#Part 3: Stations route. 
@app.route("/api/v1.0/stations")
def stations():
    
    # Station list
    session = Session(engine)
    station_list = session.query(Measurement.station).distinct().all()
    stations_list = list(np.ravel(station_list))
    
    # Return a JSON list of stations from the dataset.
    return jsonify(stations_list)


# In[135]:


#Part 4: Tobs. Query the dates and temperature observations of the most-active station for the previous year of data.

#Find most active station for previous year 

@app.route("/api/v1.0/tobs")
def tobs():
    
    session = Session(engine)
    last_date = session.query(Measurement.date).all()
    last_date = last_date[-1][0]
    last_date = dt.datetime.strptime(last_date, '%Y-%m-%d')
    last_date = last_date.date()
    one_year_date = last_date - dt.timedelta(days=365)
    
    # Query previous year Tobs
    prev_year= session.query(Measurement.date, Measurement.tobs).        filter(Measurement.date > one_year_date).all()

    # list of previous year data
    tobs_list = []

    for date, tobs in prev_year:
        tobs_dict = {}
        tobs_dict[date] = tobs
        tobs_list.append(tobs_dict) 

    #Close Session 
    session.close()

    # Return a JSON list of Tobs from previous year from the dataset.
    return jsonify(tobs_list)


# In[136]:


#Part 5a: Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for 
#a specified start or start-end range.

#For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.

@app.route('/api/v1.0/<start>')
def start (start):
    
    #Query Tobs and dates
    session = Session(enginer)
    start_date = session.query(func.min(Measurement.date)).first()[0]
    end_date = session.query(func.max(Measurement.date)).first()[0]
    
    #Identify first and last dates 
    if start >= start_date and start <= end_date:
        temps = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).            filter(Measurement.date >= start).filter(Measurement.date <= date_end).all()[0]
        
        return (
            f"Minimum Temperature: {temps[0]}</br>"
            f"Average Temperature: {calc_temps[1]}</br>"
            f"Maximum Temperature: {calc_temps[2]}")
    else: 
       #Return to JSON list of max, min, average TObs from a specified start date. 
        return jsonify()


# In[137]:


#Part 5b: For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the 

#For a start date to the end date, inclusive.

@app.route("/api/v1.0/<start>/<end>")
def start_end_date (start=None, end=None):
    
    #Query dates and Tobs
    session = Session(enginer)
    start_date = session.query(func.min(Measurement.date)).first()[0]
    end_date = session.query(func.max(Measurement.date)).first()[0]
    
    #Identify first and last dates 
    if start >= start_date and end <= end_date:
        temps = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).            filter(Measurement.date >= start).filter(Measurement.date <= date_end).all()[0]
        
        return (
            f"Minimum Temperature: {temps[0]}</br>"
            f"Average Temperature: {calc_temps[1]}</br>"
            f"Maximum Temperature: {calc_temps[2]}")
    else: 
         #Return to JSON list of max, min, average TOBs from specified start and end dates. 
        return jsonify()


# In[139]:


if __name__=="_main_":
    app.run()


# In[ ]:




