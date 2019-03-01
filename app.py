from flask import Flask
from flask import render_template
from py_files.transitHandler import *
from apscheduler.schedulers.background import BackgroundScheduler
app = Flask(__name__)


@app.route('/')
def hello_world():
    run_clock_reset()
    return render_template('index.html', header="Welcome to my Metro Transit Web App")

def run_clock_reset():
    init_map(0)
    #scheduler = BackgroundScheduler()
    #scheduler.add_job(lambda: init_map(0), trigger='interval', seconds=30)
    #scheduler.start()



if __name__ == '__main__':
    app.run()

