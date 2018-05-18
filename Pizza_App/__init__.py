from flask import Flask, render_template, url_for, request, flash, redirect, session, jsonify
#from dbconnect import connection
#from wtforms import Form
# import json


app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def homepage():

    if request.method == "POST":
        return redirect(url_for("pizza_submit"))
    data_in = {"Pizza1":[[43.082874, -77.677129]],
                   "Pizza2":[[43.0843569, -77.6821797]],
                   "Pizza3":[[43.083541, -77.677354]]}
    error="Homepage didn't load, SOOO sad"
    try:
    	return render_template("index.html", data_in=data_in)
    except Exception as e:
        return print("BRO THIS IS THE ERROR!~!", str(e))

@app.route("/pizza_submit", methods=["GET", "POST"])
def pizza_submit():
    error="Form didn't load, SOOO sad"
    if request.method =="POST":
        return redirect(url_for("homepage"))
    try:
        return render_template("form.html")
    except Exception as e:
        return print("BRO THIS IS THE ERROR!~!", str(e))


if __name__=="__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True)