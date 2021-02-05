from flask import Flask, render_template, request, jsonify
#adding time stuff
from pytz import datetime
import pytz


app = Flask(__name__)

@app.route('/profile', methods = ["POST", "GET"])
def profile_login():
    tVar = datetime.datetime.now(tz=pytz.timezone('America/Jamaica'))
    tVartoString = tVar.isoformat()
    if request.method == "POST":
        #grab data from the form 
        username = request.form["username"]
        role = request.form["role"]
        color = request.form["color"]
        if username == "Alick" and role == "Engineer" and color == "#3478ff":
            successDict = {
            "success": True,
            "data": { "last_updated": tVartoString,"username": username, "role": role, "color": color}
            }
            return jsonify(successDict)
    else:
        return render_template("login.html")

if __name__ == '__main__':
    app.run()