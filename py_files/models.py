from app import db

DB = db
class VehicleLocation(db.Model):
    BlockNumber = db.Column(db.Integer, primary_key=True)
    Route = db.Column(db.Integer)
    VehicleLatitude = db.Column(db.Float)
    VehicleLongitude = db.Column(db.Float)
    Direction = db.Column(db.Integer)

    def __init__(self, BlockNumber, Route, VehicleLatitude, VehicleLongitude, Direction):
        self.BlockNumber = BlockNumber
        self.Route = Route
        self.VehicleLatitude = VehicleLatitude
        self.VehicleLongitude = VehicleLongitude
        self.Direction = Direction


class Departure(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Actual = db.Column(db.Float)
    BlockNumber = db.Column(db.Integer)
    DepartureText = db.Column(db.String(), nullable=True)
    DepartureTime = db.Column(db.Integer)
    DepartureLatitude = db.Column(db.Float)
    DepartureLongitude = db.Column(db.Float)
    Name = db.Column(db.String(), nullable=True)

    def __init__(self, Actual, BlockNumber, DepartureText, DepartureTime, DepartureLatitude, DepartureLongitude, Name):
        self.Actual = Actual
        self.BlockNumber = BlockNumber
        self.DepartureText = DepartureText
        self.DepartureTime = DepartureTime
        self.DepartureLatitude = DepartureLatitude
        self.DepartureLongitude = DepartureLongitude
        self.Name = Name
