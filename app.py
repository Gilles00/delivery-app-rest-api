# __author__ = "Christian Barnes"

from flask_restful import Resource, Api
from flask import Flask,jsonify
from flask_jwt_extended import JWTManager

from blacklist import BLACKLIST
from models import riderModel,riderBankAccountModel, categoryModel, vehicleModel, shopModel,orderItemModel
from resources.users import UserSignup, UserLogin, UserResetUsername, UserResetPassword,UserLogout,TokenRefresh
from resources.rider import RiderSignup, RiderLogin, ActiveRiders , RiderList
from resources.vehicleResource import Vehicle_list
from resources.items import Item,ItemList,ShopItems
from resources.orders import Order, OrderList, RiderEarnings, RiderRatings
from resources.shop import Shop, SearchShop , ShopWithinRange, AllShops

from resources.delivery import Delivery
from resources.category import Category, CategoryItems, AllCategories
from resources.admin import AdminSignup, AdminLogin, AdminResetPassword, AdminResetname, ModifyShop, ModifyRider 


app = Flask(__name__)
api = Api(app)
app.config.from_object('config')


jwt = JWTManager(app)

### User enpoints
api.add_resource(UserSignup, "/usersignup")
api.add_resource(UserLogin, "/userlogin")
api.add_resource(UserResetUsername, "/usernamereset")
api.add_resource(UserResetPassword, "/userpasswordreset")
api.add_resource(TokenRefresh, '/refresh')
api.add_resource(UserLogout, '/logout')  # this is the same for everyone i.e rider and admin

### Item endpoints
api.add_resource(Item, "/item/<string:item_name>")
api.add_resource(ItemList, "/items")

### Order endpoints
api.add_resource(Order, "/order/<int:user_id>")
api.add_resource(OrderList, "/orders/<int:user_id>", "/order")


### Shop endpoints
api.add_resource(Shop, "/shops/<int:shop_id>", "/shops/")
api.add_resource(SearchShop, "/search_shops/")
api.add_resource(ShopItems, "/get_shop_items/<int:shop_id>")
api.add_resource(AllShops, "/all_shops/")
api.add_resource(ShopWithinRange, "/shop_within_range/") #still working on end point

### Delivery endpoints
api.add_resource(Delivery, "/delivery/<int:delivery_id>", "/delivery/")


### Category endpoints
api.add_resource(Category, "/category/<int:category_id>", "/category/")
api.add_resource(AllCategories, "/all_categories/")
api.add_resource(CategoryItems, "/get_category_items/<int:category_id>")


### Rider endpoints
api.add_resource(RiderSignup, "/ridersignup")
api.add_resource(RiderLogin, "/riderlogin")
api.add_resource(Vehicle_list, "/vehicles/<string:vehicle_model>")
api.add_resource(ActiveRiders, "/activeriders")
api.add_resource(RiderEarnings, "/riderearnings/<string:username>")
api.add_resource(RiderRatings, "/riderratings/<string:rider_username>")
api.add_resource(RiderList, "/riderlist")


### Adminnistrator endpoints
api.add_resource(AdminSignup, "/adminsignup")
api.add_resource(AdminLogin, "/adminlogin")
api.add_resource(AdminResetPassword, "/adminresetpassword")
api.add_resource(AdminResetname, "/adminresetname")
api.add_resource(ModifyShop, "/modifyshop")
api.add_resource(ModifyRider, "/modifyrider")



@app.after_request
def _close_db(res):
    res.headers.add('Access-Control-Allow-Origin','*')
    res.headers.add('Access-Control-Allow-Methods','POST,GET,PUT,DELETE')
    res.headers.add('Access-Control-Allow-Headers','Content-Type,Authorizaton')
    return res


# This method will check if a token is blacklisted, and will be called automatically when blacklist is enabled
@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token['jti'] in BLACKLIST


@jwt.invalid_token_loader
def invalid_token_callback(error):  # we have to keep the argument here, since it's passed in by the caller internally
    return jsonify({
        'message': 'Signature verification failed.',
        'error': 'invalid_token'
    }), 401


@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        "description": "Request does not contain an access token.",
        'error': 'authorization_required'
    }), 401


@jwt.needs_fresh_token_loader
def token_not_fresh_callback():
    return jsonify({
        "description": "The token is not fresh.",
        'error': 'fresh_token_required'
    }), 401


@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify({
        "description": "The token has been revoked.",
        'error': 'token_revoked'
    }), 401

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port= 5000,debug=True)