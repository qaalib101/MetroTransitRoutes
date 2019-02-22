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

def create_tables():
    with db:
        db.create_tables([VehicleLocation])


def replace_vehicles():
    q = VehicleLocation.delete()
    q.execute()

def add_vehicles(vehicle):
    VehicleLocation.create(
        route=vehicle['Route'],
        lat=vehicle['VehicleLatitude'],
        lon=vehicle['VehicleLongitude'],
        dir=vehicle['Direction'],
        block=vehicle['BlockNumber']
    )
class DatabaseError(Exception):
    pass