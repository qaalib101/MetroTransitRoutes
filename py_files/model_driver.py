from py_files.models import *



def replace_vehicles():
    q = VehicleLocation.delete()
    q.execute()


def replace_departures():
    q = Departure.delete()
    q.execute()


def add_vehicles(vehicles):
    for vehicle in vehicles:
        transaction = DB.session
        q = transaction.query(VehicleLocation).filter(VehicleLocation.BlockNumber == vehicle['BlockNumber']).exists()
        exists = transaction.query(q).scalar()
        if not exists:
            transaction.add(
                VehicleLocation(
                    Route=vehicle['Route'],
                    VehicleLatitude=vehicle['VehicleLatitude'],
                    VehicleLongitude=vehicle['VehicleLongitude'],
                    Direction=vehicle['Direction'],
                    BlockNumber=vehicle['BlockNumber'])
                )
        else:
            transaction.query(VehicleLocation).filter(VehicleLocation.BlockNumber == vehicle['BlockNumber']).update(vehicle)
        try:
            transaction.commit()
        except Exception as e:
            print(e)
            transaction.rollback()


def add_departures(departures):
    transaction = DB.session
    for d in departures:
        q = transaction.query(Departure).filter(VehicleLocation.block == d['BlockNumber'])
        if q.exists() is None:
            transaction.add(
                Departure(
                    Actual=d['Actual'],
                    BlockNumber=d['BlockNumber'],
                    DepartureText=d['DepartureText'],
                    DepartureTime=d['DepartureTime'],
                    DepartureLatitude=d['DepartureLatitude'],
                    DepartureLongitude=d['DepartureLongitude'],
                    Name=d['Name'])
                )
        else:
            transaction.query(Departure).filter(Departure.BlockNumber == d['BlockNumber']).update(d)
        try:
            transaction.commit()
        except Exception as e:
            print(e)
            transaction.rollback()


def get_departures():
    transaction = DB.session
    try:
        results = []
        query = transaction.query(Departure).all()
        for row in query.__dict__:
            results.append(row)
        return results
    except Exception:
        transaction.rollback()


def get_vehicles_from_database(route):
    results = []
    transaction = DB.session
    try:
        if int(route) == 0:
            query = transaction.query(VehicleLocation).all()
            for row in query.__dict__:
                results.append(row)
            return results
        else:
            query = transaction.query(VehicleLocation).filter(VehicleLocation.Route == route)
            for row in query.__dict__:
                results.append(row)
            return results
    except Exception:
        transaction.rollback()


class DatabaseError(Exception):
    pass
