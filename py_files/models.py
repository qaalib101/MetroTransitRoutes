from peewee import *

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
    if route == 0:
        vehicles = VehicleLocation.select().execute()
        return vehicles
    elif route != 0:
        try:
            vehicles = VehicleLocation.select().where(VehicleLocation.route == route)
            return vehicles
        except DoesNotExist:
            raise DatabaseError
def get_stops():
    stops = BusStop.select()
    return stops

def get_mean_locations():
    query = BusStop.select(fn.AVG(BusStop.lat).alias('meanLat'), fn.AVG(BusStop.lon).alias('meanLon'))
    query.execute(db)
    return query
class DatabaseError(Exception):
    pass
