from flask import Flask, render_template, request, jsonify, redirect, url_for
#adding time stuff
from pytz import datetime
import pytz

app = Flask(__name__)

#global dictionary to store information about a single user 
userData = {}

#global list and counter to store items related to the data route 
counter = 0
BUFFER = []

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
@app.route("/data")
def data_get():
    return jsonify(BUFFER)

@app.route("/data", methods = ["POST"])
def data_post():
    global counter
    tankTemp = request.json
    counter+=1
    tankTemp["id"] = str(counter)
    BUFFER.append(tankTemp)
    return jsonify(tankTemp)

@app.route('/data/<int:id>', methods = ["PATCH"])
def data_patch(id):
    patch = request.json
    found = False
    for dictionaries in BUFFER:
        if dictionaries["id"] == str(id):
            found = True 
            #update BUFFER 
            dictionaries["location"] = patch["location"]
            dictionaries["lat"] = patch["lat"]
            dictionaries["long"] = patch["long"]
            dictionaries["percentage_full"] = patch["percentage_full"]
            #no need to go through the rest of items if target found
            break 
    if found == False:
        #show user everything in the list if user tries to update a nonexistent record
        return redirect(url_for("data_get"))
    return jsonify(BUFFER[id-1]) #data in the list is indexed as its id - 1

@app.route('/data/<int:id>', methods = ["DELETE"])
def data_delete(id):
    BUFFER.remove(BUFFER[id-1])
    successDict = { "success":True,}
    return jsonify(successDict)


if __name__ == '__main__':
    app.run(debug=True)