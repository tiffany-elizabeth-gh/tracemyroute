'''Code to build flask app for user access and display of 
hop maps tracing an ip/web search'''

import requests
import bs4
import flask
from flask import Flask, redirect, url_for, request
import draw_map

app = Flask(__name__)

@app.route("/")
def flask_app():
    return "traceroutemap.html"

if __name__ == "__main__":
    app.run()