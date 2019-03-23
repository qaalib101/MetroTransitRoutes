from flask import Flask
from flask import render_template, flash, redirect, url_for, request, jsonify
from py_files.transitHandler import *
from apscheduler.schedulers.background import BackgroundScheduler
app = Flask(__name__)


@app.before_first_request
def run_clock_reset():
    get_all_vehicles(0)
    scheduler = BackgroundScheduler()
    scheduler.add_job(lambda: get_all_vehicles(0), trigger='interval', seconds=30)
    scheduler.start()


@app.route('/')
def index():
    return render_template('index.html', header="Welcome to my Metro Transit Web App")


@app.route('/get_map', methods=['POST'])
def get_map():
    locations = get_locations_json(request.form["radius"])
    return locations


@app.route('/get_location', methods=['GET'])
def get_location():
    location = get_user_location()
    return location


if __name__ == '__main__':
    app.config['DEBUG'] = True
    app.run(debug=True)

