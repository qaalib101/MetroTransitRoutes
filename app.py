from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from flask import render_template, flash, redirect, url_for, request, jsonify
from py_files.transitHandler import *
from apscheduler.schedulers.background import BackgroundScheduler

BASE_DIR = os.path.dirname(__file__)
app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


@app.route('/')
def index():
    return render_template('index.html', header="Welcome to my Metro Transit Web App")


@app.route('/get_map', methods=['POST'])
def get_map():
    radius = request.form["radius"]
    locations = get_locations_json(radius)
    return locations


@app.route('/get_location', methods=['GET'])
def get_location():
    location = get_user_location()
    return location


if __name__ == '__main__':
    app.run(debug=True)

