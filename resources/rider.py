# __author__ = "sarkodie"

from googlemaps import googlemaps
from flask_restful import Resource, marshal_with, fields, reqparse
from sqlalchemy.exc import SQLAlchemyError
from authentication import create_password_hash, check_password
from models.riderModel import RiderModel
from models.orderModel import OrderModel
from models.riderBankAccountModel import AccountModel
from models.vehicleModel import VehicleModel 
from blacklist import BLACKLIST

from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_refresh_token_required, 
    get_jwt_identity,
    get_raw_jwt,
    jwt_required 
)


class RiderSignup(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('rider_firstname', type=str, required=True, location='json')
        parser.add_argument('rider_lastname', type=str, required=True, location='json')
        parser.add_argument('rider_username', required =True, type=str, location='json')
        parser.add_argument('rider_email',required=True, type=str, location='json')
        parser.add_argument('rider_password', required=True, type=str, location='json')
        parser.add_argument('rider_nationality', required=True, type = str, location='json')
        parser.add_argument('rider_dateofbirth', required=True, type=str, location='json')
        parser.add_argument('rider_profilepicture', required=True, type=str, location='json')
        parser.add_argument('rider_gender', required=True, type=str, location='json')
        parser.add_argument('vehicle_licensenumber', type=str, required=True, location='json')
        parser.add_argument('vehicle_number', type=str, required=True, location='json')
        parser.add_argument('vehicle_model', required=True, type=str, location='json')
        parser.add_argument('rider_account_number', type=int, required=True, location='json')
        parser.add_argument('rider_holdername', type=str, required=True, location='json')
        data = parser.parse_args()

        if RiderModel.find_by_username(data['rider_username']):
            return {"message": "A rider with that username '{}' already exists". format(data['rider_username'])}, 400


        if RiderModel.find_by_email(data['rider_email']):
            return {"message": "A rider with that email '{}' already exists". format(data['rider_email'])}, 400

        if RiderModel.find_by_picture(data['rider_profilepicture']):
            return {"message": "A rider with that profilepicture '{}' already exists". format(data['rider_profilepicture'])}, 400

        if AccountModel.find_by_rider_account_number(data['rider_account_number']):
            return {"message": "A rider with that account number '{}' already exists". format(data['rider_account_number'])}, 400

        rider = RiderModel(data['rider_firstname'],data['rider_lastname'],data['rider_username'],
                            data['rider_email'],data['rider_password'], data['rider_nationality'],
                            data['rider_dateofbirth'],data['rider_profilepicture'],data['rider_gender'])
        rider.save_to_db() 

        account = AccountModel(data['rider_account_number'],data['rider_holdername'],rider.rider_id)
        account.save_to_db()

        vehicle = VehicleModel(data['vehicle_licensenumber'],data['vehicle_number'],data['vehicle_model'],rider.rider_id)
        vehicle.save_to_db()
        return {"message": "rider was created successfully."}, 201


class RiderLogin(Resource):     
    parser = reqparse.RequestParser()
    parser.add_argument('username', required=True, type=str, help="this field cannot be left blank")
    parser.add_argument('password', required=True, type=str, help="this field cannot be left blank")
    def post(self):

        data = RiderLogin.parser.parse_args()
        rider = RiderModel.find_by_username(data['username'])
        
        if rider and check_password(data['password'],rider):
            access_token = create_access_token(identity=rider.rider_id, fresh=True)
            refresh_token = create_refresh_token(rider.rider_id)
            rider.status = 1
            return {
                        
                       'access_token': access_token,
                       'refresh_token': refresh_token,
                       "rider_id"  : rider.rider_id
                   }, 200

        return {"message": "Invalid Credentials!"}, 401


class RiderList(Resource):
    def get(self):
        return {'riders': list(map(lambda x: x.json(), RiderModel.query.all()))}


class ActiveRiders(Resource):
    def get(self):
        return {'Activeriders': list(map(lambda x: x.json(), RiderModel.query.filter_by(status = 1)))}


class ResetRiderPassword(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('rider_password', type=str, required=True, help="this field cannot be left blank")
    parser.add_argument('newpassword', type=str, required=True, help="this field cannot be left blank")   
    
    @jwt_required
    def post(self):
        data = ResetRiderPassword.parser.parse_args() 
        rider = RiderModel.find_by_username(data['rider_username'])
        if rider:
            rider.rider_password,rider.rider_salt = create_password_hash(data['newpassword'])
            rider.save_to_db
            return {'message':'password change successful'},201
        return {'message':"password reset unsuccessful"}, 401

class ResetRiderUsername(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('rider_username', type=str, required=True, help="this field cannot be left blank")
    parser.add_argument('newusernmae', type=str, required=True, help="this field cannot be left blank")   
    
    @jwt_required
    def post(self):
        data = ResetRiderPassword.parser.parse_args() 
        rider = RiderModel.find_by_username(data['rider_username'])
        if rider:
            rider.rider_username = data['newpassword']
            rider.save_to_db()
            return {'message':'username changed successfully'},201
        return {'message':"username reset unsuccessful"}, 401


class RiderAcceptance(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('acceptState', type=bool, required=True, help="this field cannot be left blank")

    @jwt_required
    def post(self,acceptState):
        data = RiderAcceptance.parser.parse_args()
        acceptState = data['acceptState']
        if acceptState:
            return {'message': "request accepted"}
        return {'message' : "request rejected"}

    def get(self,orderid):
        order = OrderModel.find_by_id(orderid)
        return order.json()

class RidersAround(Resource):
    def get(self, shoplon, shoplat):
        data = RidersAround.parser.parse_args()
        shoplon = data['shoplon']
        shoplat = data['shoplat']
        riders = RiderModel.query.filter_by(status = 1)
        for rider in riders:
            if rider.long >= shoplon+50 and rider.long <=shopl+50 and rider.lat >=shoplat+50 and rider.lat<=shoplat+50:
                return rider