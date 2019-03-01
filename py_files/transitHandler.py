from py_files.models import *
from py_files.transit_map import *
import pandas as pd
def init_map(route):
    map = add_vehicles_and_stops_to_map(route)
    map.save('templates/map.html')
    get_stops_and_buses_location()


def get_stops_and_buses_location():
    create_tables()
    get_vehicle_locations()
    get_stop_info()


def get_vehicle_locations():
    locations = pd.read_json('http://svc.metrotransit.org/NexTrip/VehicleLocations/0?format=json', orient='columns')
    add_vehicles_to_database(locations)

def add_vehicles_to_database(locations):
    replace_vehicles()
    for index, row in locations.iterrows():
        add_vehicle(row)

def add_vehicles_and_stops_to_map(route):
    vehicles = get_vehicles(route)
    stops = get_stops()
    meanLat = 0.0
    meanLon = 0.0
    query = get_mean_locations()
    for row in query:
        meanLat = row.meanLat
        meanLon = row.meanLon
    map = get_main_map(meanLat, meanLon, vehicles, stops)
    return map

def get_stop_info():
    stops = pd.read_csv('transit_schedule/stops.txt')
    add_stops_to_database(stops)



def add_stops_to_database(stops):
    replace_stops()
    for index, row in stops.iterrows():
        add_stop(row)