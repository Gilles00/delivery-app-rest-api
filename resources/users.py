# __author__ = "Christian Barnes "


from flask_restful import Resource, marshal_with, fields, reqparse
from sqlalchemy.exc import SQLAlchemyError
from datetime import timedelta
from blacklist import BLACKLIST
from authentication import create_password_hash
from models.userModel import UserModel
from authentication import create_password_hash, check_password

from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_refresh_token_required, 
    get_jwt_identity,
    get_raw_jwt,
    jwt_required
)


class UserSignup(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('firstname', type=str, required=True, help="this field cannot be left blank")
    parser.add_argument('lastname', type=str, required=True, help="this field cannot be left blank")
    parser.add_argument('phonenumber', required=True, type=str, help="this field cannot be left blank")
    parser.add_argument('email',required=True, type=str, help="this field cannot be left blank")
    parser.add_argument('username', required=True, type=str, help="this field cannot be left blank")
    parser.add_argument('password', required=True, type=str, help="this field cannot be left blank")
    parser.add_argument('gender', required=True, type=str, help="this field cannot be left blank")
    parser.add_argument('dateofbirth', required=True, type=str, help="this field cannot be left blank")
    parser.add_argument('location', required=True, type=str, help="this field cannot be left blank")

   
    def post(self):
        data = UserSignup.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": "A user with that username already exists"}, 200
        
        if UserModel.find_by_email(data['email']):
            return {"message": "A user with that email already exists"}, 200
             
        if UserModel.find_by_phonenumber(data['phonenumber']):
            return {"message": "A user with that phonenumber already exists"}, 200


        user = UserModel(data['firstname'],data['lastname'], data['email'], data['phonenumber'], 
                         data['gender'], data['dateofbirth'][0:10], data['password'], data['username'],
                         data['location'])
        user.save_to_db()
        return {"message": "User was created successfully."}, 201


class UserLogin(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', required=True, type=str, help="this field cannot be left blank")
    parser.add_argument('password', required=True, type=str, help="this field cannot be left blank")
    def post(self):

        data = UserLogin.parser.parse_args()
        user = UserModel.find_by_username(data['username'])
        
        if user and check_password(data['password'],user):
            expires = timedelta(days=20)
            access_token = create_access_token(identity=user.user_id, fresh=True,expires_delta=expires,)
            refresh_token = create_refresh_token(user.user_id ,expires_delta=False)
            return {
                       'access_token': access_token,
                       'refresh_token': refresh_token,
                       "user_id"  : user.user_id
                   }, 200

        return {"message": "Invalid Credentials!"}, 401


class UserLogout(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        BLACKLIST.add(jti)
        return {"message": "Successfully logged out"}, 200


class UserResetPassword(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help="this field cannot be left blank")
    parser.add_argument('newpassword', type=str, required=True, help="this field cannot be left blank")   
    
   # @jwt_required
    def post(self):
        data = UserResetPassword.parser.parse_args() 
        user = UserModel.find_by_username(data['username'])
        if user:
            user.password,user.salt = create_password_hash(data['newpassword'])
            user.save_to_db()
            return {'message':'User password reset successful'},201
        return {'message':"User password reset unsuccessful"}, 401

class UserResetUsername(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help="this field cannot be left blank")
    parser.add_argument('newusername', type=str, required=True, help="this field cannot be left blank")
  
  #  @jwt_required
    def post(self):
        data = UserResetUsername.parser.parse_args()
        user = UserModel.find_by_username(data['username'])
        if user:
            user.username = data['newusername']
            user.save_to_db()
            return {'message':'Username reset successful'},201
        return {'message':"Username reset unsuccessful"}, 401

class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token': new_token}, 200