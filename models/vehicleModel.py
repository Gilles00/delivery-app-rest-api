# __author__ = "sarkodie"


from db import db

class VehicleModel(db.Model):
    __tablename__ = 'vehicle'

    vehicle_id = db.Column(db.Integer, primary_key =True)
    vehicle_licensenumber = db.Column(db.String(50))
    vehicle_number = db.Column(db.String(14))
    vehicle_model = db.Column(db.String(100))
  
    rider_id = db.Column(db.Integer, db.ForeignKey('rider.rider_id'), nullable = False)
    rider = db.relationship('RiderModel')


    def __init__(self, vehicle_licensenumber, vehicle_number, vehicle_model,rider_id):
        self.vehicle_licensenumber = vehicle_licensenumber
        self.vehicle_number = vehicle_number
        self.vehicle_model = vehicle_model
        self.rider_id = rider_id

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_vehicle_number(cls, name):
        return cls.query.filter_by(vehicle_number = name).first()

    @classmethod   ## finding vehicle records in the db by vehicle model
    def find_by_vehicle_model(cls, name):
        return cls.query.filter_by(vehicle_model = name).all()
