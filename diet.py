from flask import Flask,render_template, url_for ,flash , redirect
import joblib
from flask import request
import numpy as np


import os
from flask import send_from_directory

app=Flask(__name__,template_folder='dietchart')

#@app.route("/")

@app.route("/")
def home():
    return render_template("mini_project2.html")
 

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
    if request.method == 'POST':
        to_predict_list = request.form.to_dict()
        to_predict_list=list(to_predict_list.values())
        to_predict_list = list(map(float, to_predict_list))
        if(len(to_predict_list)==8):#Daiabtes
            result = ValuePredictor(to_predict_list,8)
            if(int(result) == 1):
                return (render_template("diabetes.html",prediction = "fe"))

        elif(len(to_predict_list)==12):#kidney
            result = ValuePredictor(to_predict_list,12)
            if(int(result) == 1):
                return (render_template("kidney.html",prediction = prediction))

        elif(len(to_predict_list)==11):#heart
            result = ValuePredictor(to_predict_list,11)
            if(int(result) == 1):
                return (render_template("heart.html",prediction = prediction))
            
    if(int(result)!=1):
        return (render_template("heart.html"))
        #prediction='Sorry ! Suffering'
    #else:
        #prediction='Congrats ! you are Healthy' 
    return(render_template("diabetes.html"))


if __name__ == "__main__":
    app.run(debug=True)