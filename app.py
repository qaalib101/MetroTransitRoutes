from flask import Flask
from flask import render_template, request, redirect
import requests
from peewee import *
app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('index.html', header="Welcome to my Metro Transit Web App")
def get_routes():
    requests.get()
if __name__ == '__main__':
    app.run()
