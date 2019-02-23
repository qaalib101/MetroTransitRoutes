from models import *
import pandas as pd


def get_vehicle_locations():
    locations = pd.read_json('http://svc.metrotransit.org/NexTrip/VehicleLocations/0?format=json', orient='columns')
    add_to_database(locations)

def add_to_database(locations):
    create_tables()
    replace_vehicles()
    for index, row in locations.iterrows():
        add_vehicles(row)
