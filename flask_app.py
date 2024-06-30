'''Code to build flask app for user access and display of 
hop maps tracing an ip/web search'''

import requests
import bs4
import flask
from flask import Flask
import draw_map

app = Flask(__name__)

@app.route("/")
def flask_app():
    '''Function to display the flask app'''
    return flask.render_template("traceroutemap.html", title="Trace My Route")

app.run(debug=False, port=8080)