# __author__ = "Christian Barnes "


from flask_restful import Resource, reqparse
from sqlalchemy.exc import SQLAlchemyError
from flask import jsonify
from datetime import timedelta

from blacklist import BLACKLIST
from authentication import create_password_hash
from models.adminModel import AdminModel
from models.shopModel import ShopModel
from models.riderModel import RiderModel
from models.vehicleModel import VehicleModel 
from models.riderBankAccountModel import AccountModel

from authentication import create_password_hash, check_password

from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_refresh_token_required, 
    get_jwt_identity,
    get_raw_jwt,
    jwt_required
)

class AdminSignup(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('firstname', type=str, required=True, help="this field cannot be left blank")
    parser.add_argument('lastname', type=str, required=True, help="this field cannot be left blank")
    parser.add_argument('phonenumber', required=True, type=str, help="this field cannot be left blank")
    parser.add_argument('email',required=True, type=str, help="this field cannot be left blank")
    parser.add_argument('adminname', required=True, type=str, help="this field cannot be left blank")
    parser.add_argument('password', required=True, type=str, help="this field cannot be left blank")
    parser.add_argument('nationality', required=True, type=str, help="this field cannot be left blank")

    def post(self):
        data = AdminSignup.parser.parse_args()

        if AdminModel.find_by_username(data['adminname']):
            return {"message": "A admin with that adminname already exists"}, 400
        
        if AdminModel.find_by_email(data['email']):
            return {"message": "A admin with that email already exists"}, 400



        admin = AdminModel(data['firstname'],data['lastname'], data['adminname'], data['email'], data['nationality'], data['password'])#, data['gender'], data['phonenumber'], data['dateofbirth'], data['profilepicture'])
        admin.save_to_db()
        return {"message": "admin was created successfully."}, 201


class AdminLogin(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('adminname', required=True, type=str, help="this field cannot be left blank")
    parser.add_argument('password', required=True, type=str, help="this field cannot be left blank")
    def post(self):

        data = AdminLogin.parser.parse_args()
        admin = AdminModel.find_by_username(data['adminname'])
        
        if admin and check_password(data['password'],admin):
            expires = timedelta(days=20)
            access_token = create_access_token(identity=admin.admin_id, fresh=True,expires_delta=expires)
            refresh_token = create_refresh_token(admin.admin_id ,expires_delta=False)
            return {
                       'access_token': access_token,
                       'refresh_token': refresh_token,
                       "admin_id"  : admin.admin_id
                   }, 200
        return {"message": "Invalid Credentials!"}, 401


class AdminResetPassword(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('adminname', type=str, required=True, help="this field cannot be left blank")
    parser.add_argument('newpassword', type=str, required=True, help="this field cannot be left blank")   
    
   # @jwt_required
    def post(self):
        data = AdminResetPassword.parser.parse_args() 
        admin = AdminModel.find_by_adminname(data['adminname'])
        if admin:
            admin.password,admin.salt = create_password_hash(data['newpassword'])
            admin.save_to_db()
            return {'message':'admin password reset successful'},201
        return {'message':"admin password reset unsuccessful"}, 401

class AdminResetname(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('adminname', type=str, required=True, help="this field cannot be left blank")
    parser.add_argument('newadminname', type=str, required=True, help="this field cannot be left blank")
  
  #  @jwt_required
    def post(self):
        data = AdminResetname.parser.parse_args()
        admin = AdminModel.find_by_adminname(data['adminname'])
        if admin:
            admin.adminname = data['newadminname']
            admin.save_to_db()
            return {'message':'Adminname reset successful'},201
        return {'message':"Adminname reset unsuccessful"}, 401


class ModifyShop(Resource):
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('shop_name', type=str, required=True, location='json')
        parser.add_argument('shop_location', type=str, required=True, location='json')
        parser.add_argument('shop_coordinates', required=True, type=int, location='json')
        parser.add_argument('shop_description', required=True, type=int, location='json')
        
        data = parser.parse_args()

        shop = ShopModel.find_by_name(data['shop_name'])

        if shop:
            shop.price = data['price']
        else:
            shop = ShopModel(data['shop_name'], **data)

        shop.save_to_db()

        return{"message":"Shop addition successful"}


    def delete(self,shop_id):
        data = ShopModel.query.get(shop_id)

        if data is None:
            return jsonify(
                {'message': "Shop Not Found"})
        
        data.delete_from_db()
        return jsonify(
            {'message': "Shop was successfully deleted"}
        ) 

class ModifyRider(Resource):
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('rider_firstname', type=str, required=True, location='json')
        parser.add_argument('rider_lastname', type=str, required=True, location='json')
        parser.add_argument('rider_adminname', required =True, type=str, location='json')
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

        if RiderModel.find_by_name(data['rider_adminname']):
            return {"message": "A rider with that adminname '{}' already exists". format(data['rider_adminname'])}, 400
     
        if RiderModel.find_by_email(data['rider_email']):
            return {"message": "A rider with that email '{}' already exists". format(data['rider_email'])}, 400

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

        return{"message":"Rider addition successful"}


    def delete(self,rider_id):
        data = RiderModel.query.get(rider_id)

        if data is None:
            return{'error': "Rider Not Found"}
        
        data.delete_from_db()
        return{'message': "Rider was successfully deleted"}
        
