from py_files.model_driver import *
from py_files.transit_map import *
import pandas as pd
import json
from multiprocessing.dummy import Pool as ThreadPool
from threading import Thread


def get_locations_json(radius):
    #get_metro_transit_zip_folder()
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

    # return json.dumps(return_json)
    return 0


def add_vehicles_and_departures():
    add_vehicles_to_database()
    add_departures_to_database()
    print("added to database")


def add_departures_to_database():
    stops = get_stop_info()
    departures = get_departures(stops)
    add_departures(departures)


def get_user_location():
    location = get_location()
    json_location = json.dumps(location)
    return json_location


def add_vehicles_to_database():
    vehicles = get_all_vehicles(0)
    add_vehicles(vehicles)


def run_threads():
    pool = ThreadPool(2)
    pool.map_async()

