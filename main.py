from flask import Flask, render_template, request, jsonify, redirect, url_for
#adding time stuff
from pytz import datetime
import pytz

successDIct = {}
app = Flask(__name__)

userData = {}

#Profile  Routes 
@app.route('/profile')
def profile_get():
    return render_template("login.html")

@app.route('/profile', methods = ['POST'])
def profile_post():
    #obtain time stamp
    tVar = datetime.datetime.now(tz=pytz.timezone('America/Jamaica'))
    tVartoString = tVar.isoformat()
    #obtain json object from the request object
    userD = request.json
    #do the validation 
    if userD["username"] == "Alick" and userD["role"] == "Engineer" and userD["color"] == "#3478ff":
        #credentials are correct so update global dictionary to shpw that Alick has logged in
        global userData
        userData = userD
        #append time stamp to local dictionary and prepare for return
        userD["last_updated"] = tVartoString
        successDict = {
            "successs":True,
            "data": userD
        }
        return jsonify(successDict)
    else:
        return redirect(url_for("profile_get"))

@app.route('/profile', methods = ["PATCH"])
def profile_patch():
    global userData #this global variable will be updated locally
    #obtain time stamp
    tVar = datetime.datetime.now(tz=pytz.timezone('America/Jamaica'))
    tVartoString = tVar.isoformat()
    #obtain json object from the request object in a local dictionary
    userD = request.json   
    #user can only patch if the profile has already been created
    #Therefore, check if global dictionary has correct credentials in it
    if userData["username"] == "Alick" and userData["role"] == "Engineer" and userData["color"] == "#3478ff":
        #credentials are correct so patch global dictionary
        userData = userD
        #append time stamp to local dictionary and prepare for return
        userD["last_updated"] = tVartoString
        successDict = {
        "successs":True,
        "data": userD
        }            
        return jsonify(successDict)
    else:
        return redirect(url_for("profile_get"))

#Data Routes 

if __name__ == '__main__':
    app.run(debug=True)