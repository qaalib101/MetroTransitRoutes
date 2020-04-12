from app import db
from playhouse.shortcuts import model_to_dict


class VehicleLocation(db.Model):
    block = db.Column(db.Integer, primary_key=True)
    route = db.Column(db.Integer)
    lat = db.Column(db.Float)
    lon = db.Column(db.Float)
    dir = db.Column(db.Integer)

    def __init__(self, block, route, lat, lon, dir):
        self.block = block
        self.route = route
        self.lat = lat
        self.lon = lon
        self.dir = dir


class Departure(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    actual = db.Column(db.Float)
    block = db.Column(db.Integer)
    dText = db.Column(db.String(), nullable=True)
    dTime = db.Column(db.Integer)
    stop_lat = db.Column(db.Float)
    stop_lon = db.Column(db.Float)
    name = db.Column(db.String(), nullable=True)

    def __init__(self, actual, block, dText, dTime, stop_lat, stop_lon, name):
        self.actual = actual
        self.block = block
        self.dText = dText
        self.dTime = dTime
        self.stop_lat = stop_lat
        self.stop_lon = stop_lon
        self.name = name


def create_tables():
    with db:
        db.create_all()


def replace_vehicles():
    q = VehicleLocation.delete()
    q.execute()


def replace_departures():
    q = Departure.delete()
    q.execute()


def add_vehicles(vehicles):

    with db.session() as transaction:
        for vehicle in vehicles:
            transaction.add(
                VehicleLocation(
                    route=vehicle['Route'],
                    lat=vehicle['VehicleLatitude'],
                    lon=vehicle['VehicleLongitude'],
                    dir=vehicle['Direction'],
                    block=vehicle['BlockNumber'])
            )
        try:
            transaction.commit()
        except Exception as e:
            print(e)
            transaction.rollback()


def add_departures(departures):
    with db.session() as transaction:
        for d in departures:
            transaction.add(
                Departure(
                    actual=d['Actual'],
                    block=d['BlockNumber'],
                    dText=d['DepartureText'],
                    dTime=d['DepartureTime'],
                    stop_lat=d['lat'],
                    stop_lon=d['lon'],
                    name=d['name'])
            )
        try:
            transaction.commit()
        except Exception as e:
            print(e)
            transaction.rollback()


def get_departures():
    with db.session() as transaction:
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
        except Exception:
            transaction.rollback()


def get_vehicles_from_database(route):
    with db.session() as transaction:
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
        except Exception:
            transaction.rollback()


class DatabaseError(Exception):
    pass
