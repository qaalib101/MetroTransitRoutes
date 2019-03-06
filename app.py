from flask import Flask
from flask import render_template, flash, redirect, url_for, request
from py_files.transitHandler import *
import peewee
from apscheduler.schedulers.background import BackgroundScheduler
app = Flask(__name__)

@app.before_first_request
def run_clock_reset():
    scheduler = BackgroundScheduler()
    scheduler.add_job(lambda: add_vehicles_to_database(0), trigger='interval', seconds=30)
    scheduler.add_job(lambda: init_map(0), trigger='interval', seconds=30)
    scheduler.start()

@app.route('/')
def index():
    routes = get_routes_from_database()
    return render_template('index.html', header="Welcome to my Metro Transit Web App", routes=routes)

@app.route('/get_map', methods=['POST'])
def get_map():
    try:
        route = request.form['routes']
        print(route)
        init_map(route)
        return render_template('map_holder.html')
    except peewee.DoesNotExist:
        flash('Route was not found')
        return redirect('/')

if __name__ == '__main__':
    app.jinja_environment.auto_reload = True
    app.jinja_env.cache = 0
    app.jinja_env.auto_reload = Tru
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.run(debug=True)

