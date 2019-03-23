from peewee import *
from playhouse.shortcuts import model_to_dict
db = SqliteDatabase('metro_buses.db')


class BaseModel(Model):

    class Meta:
        database = db


class VehicleLocation(BaseModel):
    block = IntegerField()
    route = IntegerField()
    lat = FloatField()
    lon = FloatField()
    dir = IntegerField()



class Departure(BaseModel):
    actual = BooleanField()
    block = IntegerField()
    dText = CharField(null=True)
    dTime = IntegerField()
    stoplat = FloatField()
    stoplon = FloatField()
    name = CharField(null=True)



def create_tables():
    with db:
        db.create_tables([VehicleLocation, Departure])


def replace_vehicles():
    q = VehicleLocation.delete()
    q.execute()


def replace_departures():
    q = Departure.delete()
    q.execute()


def add_vehicle(vehicle):
    with db.atomic() as transaction:
        try:
            VehicleLocation.create(
                route=vehicle['Route'],
                lat=vehicle['VehicleLatitude'],
                lon=vehicle['VehicleLongitude'],
                dir=vehicle['Direction'],
                block=vehicle['BlockNumber']
            )
        except OperationalError as e:
            transaction.rollback()



def add_departure(d):
    with db.atomic() as transaction:
        try:
            Departure.create(
                actual=d['Actual'],
                block=d['BlockNumber'],
                dtext=d['DepartureText'],
                dTime=d['DepartureTime'],
                stoplat=d['lat'],
                stoplon=d['lon'],
                name=d['name']
            )
        except OperationalError as e:
            transaction.rollback()


def get_departures():
    with db.atomic() as transaction:
        try:
            results = []
            query = Departure.select()
            cursor = db.execute(query)
            ncols = len(cursor.description)
            colnames = [cursor.description[i][0] for i in range(ncols)]
            for row in cursor.fetchall():
                res = {}
                for i in range(ncols):
                    res[colnames[i]] = row[i]
                results.append(res)
            return results
        except OperationalError:
            transaction.rollback()



def get_vehicles_from_database(route):
    with db.atomic() as transaction:
        try:
            if int(route) == 0:
                results = []
                query = VehicleLocation.select()
                cursor = db.execute(query)
                ncols = len(cursor.description)
                colnames = [cursor.description[i][0] for i in range(ncols)]
                for row in cursor.fetchall():
                    res = {}
                    for i in range(ncols):
                        res[colnames[i]] = row[i]
                    results.append(res)
                return results
        except OperationalError:
            transaction.rollback()



class DatabaseError(Exception):
    pass
