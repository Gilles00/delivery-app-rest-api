# __author__ = "sarkodie"


from flask_restful import Resource, fields, reqparse, request
from sqlalchemy.exc import SQLAlchemyError
from models.vehicleModel import VehicleModel


class Vehicle(Resource):
    def get(self, vehicle_model):
        VehicleModel.find_by_vehicle_model(vehicle_model)
        


class Vehicle_list(Resource):
    # def get(self, vehicle_number):
    #     return {'vehicles': list(map(lambda x: x.json(), VehicleModel.query.filter_by(vehicle_number=vehicle_number)))}

    def get(self, vehicle_model):
        return {'vehicles': list(map(lambda x: x.json(), VehicleModel.query.filter_by(vehicle_model=vehicle_model)))}
