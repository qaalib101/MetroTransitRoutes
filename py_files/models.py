from peewee import *
from playhouse.shortcuts import model_to_dict
db = SqliteDatabase('metro_buses.db')


class BaseModel(Model):

    class Meta:
        database = db


class VehicleLocation(BaseModel):
    route = IntegerField()
    lat = DecimalField(max_digits=10)
    lon = DecimalField(max_digits=10)
    dir = IntegerField()
    block = IntegerField()


class BusStop(BaseModel):
    stopID = PrimaryKeyField(unique=True)
    name = CharField()
    lat = DecimalField(max_digits=10)
    lon = DecimalField(max_digits=10)


def create_tables():
    with db:
        db.create_tables([VehicleLocation, BusStop])


def replace_vehicles():
    q = VehicleLocation.delete()
    q.execute()


def replace_stops():
    q = BusStop.delete()
    q.execute()


def add_vehicle(vehicle):
    VehicleLocation.create(
        route=vehicle['Route'],
        lat=vehicle['VehicleLatitude'],
        lon=vehicle['VehicleLongitude'],
        dir=vehicle['Direction'],
        block=vehicle['BlockNumber']
    )


def add_stop(stop):
    BusStop.create(
        stopID=stop['stop_id'],
        name=stop['stop_name'],
        lat=stop['stop_lat'],
        lon=stop['stop_lon'],
    )


def get_vehicles(route):
    with db.atomic() as transaction:
        try:
            if int(route) == 0:
                vehicles = VehicleLocation.select().execute()
                return vehicles
            else:
                vehicles = VehicleLocation.select().where(VehicleLocation.route == route)
                return vehicles
        except OperationalError:
            transaction.rollback()


def get_stops():
    stops = BusStop.select()
    return stops


def get_routes():
    query = VehicleLocation.select(VehicleLocation.route).group_by(VehicleLocation.route)
    routes = [row for row in query]
    return routes

def get_mean_locations():
    query = VehicleLocation.select(fn.AVG(VehicleLocation.lat).alias('meanLat'), fn.AVG(VehicleLocation.lon).alias('meanLon'))
    query.execute(db)
    return query


class DatabaseError(Exception):
    pass
