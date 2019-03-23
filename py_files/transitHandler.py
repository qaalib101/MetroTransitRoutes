from py_files.models import *
from py_files.transit_map import *
import pandas as pd
import json


def get_locations_json(radius):
    stops = get_stop_info()
    radius = float(radius)
    location = get_location()
    vehicles = get_vehicles_from_database(0)
    near_stops = filter_stops(stops, location, radius)
    departures = get_departures(near_stops)
    departures = order_departures(departures, ['BlockNumber', 'DepartureTime'])
    near_vehicles = get_vehicles(departures, vehicles)
    return_json = {
        "center": location,
        "departures": departures,
        "vehicles": near_vehicles
    }
    return json.dumps(return_json)


def add_departures_to_database(departures):
    for d in departures:
        add_departure(d)

def get_user_location():
    location = get_location()
    json_location = json.dumps(location)
    return json_location


def add_vehicles_to_database(vehicles):
    replace_vehicles()
    for i, row in vehicles.iterrows():
        add_vehicle(row)

def get_all_vehicles(route):
    vehicles = pd.read_json(f'http://svc.metrotransit.org/NexTrip/VehicleLocations/{route}?format=json')
    create_tables()
    add_vehicles_to_database(vehicles)

def get_stop_info():
    stops = pd.read_csv('transit_schedule/stops.txt')
    return stops

