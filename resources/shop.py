# __author__ = "Kimberly"


from flask_restful import Resource, Api, abort, reqparse
from models.shopModel import ShopModel
from flask import jsonify
from flask import request
from db import db
from math import acos,cos,sin,pi

#

def great_circle_distance(coordinates1, coordinates2):
                latitude1, longitude1 = coordinates1
                latitude2, longitude2 = coordinates2
                d = pi / 180  # factor to convert degrees to radians
                return acos(sin(longitude1*d) * sin(longitude2*d) +
                        cos(longitude1*d) * cos(longitude2*d) *
                        cos((latitude1 - latitude2) * d)) / d

def in_range(coordinates1, coordinates2, range):
                return great_circle_distance(coordinates1, coordinates2) < range


class Shop(Resource):
    def get(self, shop_id):
        data = ShopModel.query.get(shop_id)
     
        if data is None:
            return jsonify(
                {'error': "Shop Not Found"}
            )
        else:
            return jsonify({
                'shop_id': data.shop_id,
                'shop_name': data.shop_name,
                'shop_location': data.shop_location,
                'shop_coordinates': data.shop_coordinates,
                'shop_description': data.shop_description
            })

    def post(self):
        json_data = request.get_json(force=True)

        if json_data is None:
            return jsonify(
                {'error': "No data was inserted"}
            )

        shopp = ShopModel(name=json_data['shop_name'],
                          location=json_data['shop_location'],
                          coordinates=json_data['shop_coordinates'],
                          description=json_data['shop_description'])
        db.session.add(shopp)
        db.session.commit()
        return jsonify({'message': 'New shop successfully created'})

    def delete(self, shop_id):
        data = ShopModel.query.get(shop_id)

        if data is None:
            return jsonify(
                {'error': "Shop Not Found"})
        
        db.session.delete(data)
        db.session.commit()
        return jsonify(
            {'message': "Shop was successfully deleted"}
        )


class SearchShop(Resource):

    def post(self):
        json_data = request.get_json(force=True)
        shopName = json_data["searchterm"]
        data = ShopModel.query.filter_by(shop_name=shopName).first()
        if data is None:
            return jsonify(
                {'error': "Shop Not Found"}
            )
        else:
            return jsonify({
                'shop_id': data.shop_id,
                'shop_name': data.shop_name,
                'shop_location': data.shop_location,
                'shop_coordinates': data.shop_coordinates,
                'shop_description': data.shop_description})
    
class AllShops(Resource):
        def get(self):
            return {'shops': list(map(lambda x: x.json(), ShopModel.query.all()))}

            
#function not ready
class ShopWithinRange(Resource): 
    def post(self):
        json_data = request.get_json(force=True)
        shopCoordinates = json_data["shop_coordinates"]
        remove = shopCoordinates.replace(" ","")
        data = ShopModel.query.filter_by(shop_coordinates=remove).first()
        # a = 3
        # def fun(a, n):
        #     if n < a:
        #         return(str(n).zfill(a))
        # var = fun(a, 2)
        # print var
        if data is None:
            return jsonify({
                'error': "Shop Not Found"
            })
        else:
            in_range(data, coordinates2, range)
             

            

            # return jsonify({
            #     'shop_coordinates' : data.shop_coordinates
            # })

    # def get(self, longitude, latitude ):
    #     data = ShopModel.query.filter_by().all()
    #     print data

