from flask import Flask, render_template, url_for, request, flash, redirect, session, jsonify
#from dbconnect import connection
#from wtforms import Form
# import json


app = Flask(__name__)

@app.route("/")
def homepage():
    error="Homepage didn't load, SOOO sad"
    try:
    	# return "It worked!"
    	return render_template("index.html")
    except Exception as e:
        return print("BRO THIS IS THE ERROR!~!", str(e))

@app.route("/pizza_submit")
def form():
    error="Form didn't load, SOOO sad"
    try:
    	# return "It worked!"
    	return render_template("form.html")
    except Exception as e:
        return print("BRO THIS IS THE ERROR!~!", str(e))


if __name__=="__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True)