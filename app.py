from flask import Flask
from flask import render_template, request, redirect
from transitHandler import *
from apscheduler.schedulers.background import BackgroundScheduler
app = Flask(__name__)


@app.route('/')
def hello_world():
    get_vehicle_locations()
    run_clock_reset()
    return render_template('index.html', header="Welcome to my Metro Transit Web App")
def run_clock_reset():
    scheduler = BackgroundScheduler()
    scheduler.add_job(get_vehicle_locations, 'cron', second=30)
    scheduler.start()
if __name__ == '__main__':
    app.run()

