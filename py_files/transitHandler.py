from py_files.models import *
from py_files.transit_map import *
import pandas as pd
import json
from multiprocessing.dummy import Pool as ThreadPool
from threading import Thread


def get_locations_json(radius):
    get_metro_transit_zip_folder()
    # stops = get_stop_info()
    # radius = float(radius)
    # location = get_location()
    # vehicles = get_all_vehicles(0)
    # near_stops = filter_stops(stops, location, radius)
    # departures = get_departures(near_stops)
    # departures = order_departures(departures, ['BlockNumber', 'DepartureTime'])
    # near_vehicles = get_vehicles(departures, vehicles)
    # thread = Thread(target=add_vehicles_and_departures, args=(near_vehicles, departures))
    # thread.start()
    # thread.join()
    # return_json = {
    #     "center": location,
    #     "departures": departures,
    #     "vehicles": near_vehicles
    # }

    return json.dumps(return_json)


def add_vehicles_and_departures(vehicles, departures):
    create_tables()
    add_vehicles_to_database(vehicles)
    add_departures_to_database(departures)
    print("added to database")


def add_departures_to_database(departures):
    add_departures(departures)


def get_user_location():
    location = get_location()
    json_location = json.dumps(location)
    return json_location


def add_vehicles_to_database(vehicles):

    add_vehicles(vehicles)


def get_all_vehicles(route):
    vehicles = requests.get(f'http://svc.metrotransit.org/NexTrip/VehicleLocations/{route}?format=json')
    return vehicles.json()


def get_stop_info():

    stops = pd.read_csv('transit_schedule/stops.txt')
    return stops


def run_threads():
    pool = ThreadPool(2)
    pool.map_async()

