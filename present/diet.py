from flask import Flask,render_template, url_for ,flash , redirect
import joblib
from flask import request
import numpy as np
from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
import googlemaps
from googlemaps.exceptions import ApiError
import requests
from googleplaces import GooglePlaces, types, lang


import os
from flask import send_from_directory

app=Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'

@app.route("/")
def welcome():
    return render_template("index.html")

@app.route("/landing")
def landing():
    return render_template("landing.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/register")
def register():
    return render_template("dietchart.html")
 

@app.route("/diabetes")
def diabetes():
    #if form.validate_on_submit():
    return render_template("diabetes.html")

@app.route("/heart")
def heart():
    return render_template("heart.html")


@app.route("/kidney")
def kidney():
    #if form.validate_on_submit():
    return render_template("kidney.html")

def ValuePredictor(to_predict_list, size):
    to_predict = np.array(to_predict_list).reshape(1,size)
    if(size==8):#Diabetes
        loaded_model = joblib.load("model1")
        result = loaded_model.predict(to_predict)
    elif(size==12):#Kidney
        loaded_model = joblib.load("model3")
        result = loaded_model.predict(to_predict)
    elif(size==11):#Heart
        loaded_model = joblib.load("model2")
        result =loaded_model.predict(to_predict)
    return result[0]

@app.route('/result',methods = ["POST"])
def result():
    result = 0
    if request.method == 'POST':
        to_predict_list = request.form.to_dict()
        to_predict_list=list(to_predict_list.values())
        to_predict_list = list(map(float, to_predict_list))
        #return "len(to_predict_list)"
        print("adsd" ,len(to_predict_list))
        if(len(to_predict_list)==8):#Daiabtes
            result = ValuePredictor(to_predict_list,8)
            print(result)
            if(int(result) == 1):
                return (render_template("chart1.html"))

        elif(len(to_predict_list)==12):#kidney
            result = ValuePredictor(to_predict_list,12)
            if(int(result) == 1):
                return (render_template("chart2.html"))

        elif(len(to_predict_list)==11):#heart
            result = ValuePredictor(to_predict_list,11)
            if(int(result) == 1):
                return (render_template("chart3.html"))
            
    if(int(result)!=1):
        return (render_template("chart2.html"))
    #if(int(result) == 1):
        #prediction='Sorry ! Suffering'
    #else:
        #prediction='Congrats ! you are Healthy' 
    return(render_template("chart2.html"))

'''
def find_nearest_hospital(location):
    # Build the Google Maps API query URL
    url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
    params = {
        'location': location,
        'radius': 1000000000,
        'type': 'hospital',
        'key': 'YOUR_API_KEY'
    }

    # Send the API request and parse the response
    response = requests.get(url, params=params).json()
    results = response.get('results', [])

    # Sort the results by distance from the user's location
    results.sort(key=lambda r: r.get('distance', float('inf')))

    # Return the location of the nearest hospital
    if results:
        nearest = results[0]
        lat = nearest['geometry']['location']['lat']
        lng = nearest['geometry']['location']['lng']
        return f'{lat},{lng}'
    else:
        return None
'''

def find_nearest(log,lat):
    API_KEY = 'Your_API_Key'
    google_places = GooglePlaces(API_KEY)
    query_result = google_places.nearby_search(
    lat_lng ={'lat': lat, 'lng': log},
    radius = 5000,
    types =[types.TYPE_HOSPITAL])

    return query_result


class LocationForm(FlaskForm):
    location = StringField('Location', validators=[DataRequired()])


@app.route("/loc")
def ind():
    return  render_template("nearest_location.html")

@app.route("/lokie",methods = ["POST"])
def index():
    form = LocationForm()
    #print(form.latitude)
    if request.method == "POST":
        latitude = request.form.get("latitude")
        longitude = request.form.get("longitude")
        nearest_hospital = find_nearest(latitude, longitude)
        #print(nearest_hospital)
        if nearest_hospital.has_attributions:
            return f'The nearest hospital is.'
        else:
            return 'No hospital found.'
    
    return  "welcome"






if __name__ == "__main__":
    app.run(debug=True)