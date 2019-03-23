import requests
import math
import json
from operator import itemgetter
import os
import functools
from re import sub, split
import pandas as pd
def get_location():
    API_KEY = os.environ['GEO_API_KEY']
    send_url = f'http://api.ipstack.com/check?access_key={API_KEY}'
    geo_req = requests.get(send_url)
    geo_json = json.loads(geo_req.text)
    location = {"lat": geo_json['latitude'], "lon": geo_json['longitude']}
    return location


def order_departures(items, columns):
    comparers = [((itemgetter(col[1:].strip()), -1) if col.startswith('-') else
                  (itemgetter(col.strip()), 1)) for col in columns]

    def comparer(left, right):
        for fn, mult in comparers:
            result = cmp(fn(left), fn(right))
            if result:
                return mult * result
            else:
                return 0

    return sorted(items, key=functools.cmp_to_key(comparer))


def cmp(a, b):
    return (a > b) - (a < b)


def get_departures(stops):
    departures = []
    for stop in stops:
        id = stop['id']
        lat = stop['lat']
        lon = stop['lon']
        name = stop['name']
        req = requests.get(f'http://svc.metrotransit.org/NexTrip/{id}?format=json')
        data = req.json()
        for d in data:
            if d == data[4]:
                break
            unix = d['DepartureTime'].split('-')[0]
            unix = sub("[^0-9]", "", unix)
            d['DepartureTime'] = unix
            d['lat'] = lat
            d['lon'] = lon
            d['name'] = name
        if len(data) > 0:
            departures.extend(data)
        if len(departures) > 2000:
            break
    return departures


def get_vehicles(departures, vehicles):
    blocks =[d['BlockNumber'] for d in departures]
    filtered_vehicles = [d for d in vehicles if d['block'] in blocks]
    return filtered_vehicles


def filter_stops(stops, location, miles):
    locations = []
    for i, row in enumerate(stops.itertuples()):
        degrees = miles/60.0
        vlat = float(row.stop_lat)
        vlon = float(row.stop_lon)
        stop = {
            "id": row.stop_id,
            "name": row.stop_name,
            "lat": vlat,
            "lon": vlon
        }
        if return_distance(degrees, location, vlat, vlon):
            locations.append(stop)
    return locations


def filter_vehicles(vehicles, location, miles):
    locations = []
    for i, row in enumerate(vehicles.itertuples()):
        degrees = miles/60.0
        vlat = float(row.stop_lat)
        vlon = float(row.stop_lon)
        stop = {
            "id": row.stop_id,
            "name": row.stop_name,
            "lat": vlat,
            "lon": vlon
        }
        if return_distance(degrees, location, vlat, vlon):
            locations.append(stop)
    return locations



def return_distance(degrees, location, lat, lon):
    distance = math.sqrt((location["lat"] - lat) ** 2 + (location["lon"] - lon) ** 2)
    return True if distance <= degrees else False
