from py_files.models import *
from py_files.transit_map import *
import pandas as pd
import os
def init_map(route):
    vehicles = get_vehicles(route)
    map = add_vehicles_and_stops_to_map(vehicles)



def get_routes_from_database():
    routes = get_routes()
    return routes
def get_vehicle_locations(route):
    locations = pd.read_json(f'http://svc.metrotransit.org/NexTrip/VehicleLocations/{route}?format=json', orient='columns')
    return locations

def add_vehicles_to_database(route):
    locations = get_vehicle_locations(route)
    replace_vehicles()
    for index, row in locations.iterrows():
        add_vehicle(row)

def add_vehicles_and_stops_to_map(vehicles):
    query = get_mean_locations()
    meanLon = 0.0
    meanLat = 0.0
    for row in query:
        meanLat = row.meanLat
        meanLon = row.meanLon
    map = get_main_map(meanLat, meanLon, vehicles)
    return map

def get_stop_info():
    stops = pd.read_csv('transit_schedule/stops.txt')
    return stops


def add_stops_to_database(stops):
    replace_stops()
    for index, row in stops.iterrows():
        add_stop(row)