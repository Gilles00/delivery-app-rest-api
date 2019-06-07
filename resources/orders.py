# __author__ = "Crhistian Barnes "


from flask_restful import Resource, reqparse
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func
from models.orderModel import OrderModel
from models.orderItemModel import OrderItemModel
from models.itemModel import ItemModel
from models.deliveryModel import DeliveryModel
from models.riderModel import RiderModel

from flask import jsonify


class Order(Resource):
   
    def get(self,user_id):
        order = OrderModel.find_by_id(user_id)
        if order: 
            return order.json()
        return {"message":"No order has been found"},401

    def post(self,user_id):        
        parser = reqparse.RequestParser()
        parser.add_argument('destination', type=str, required=True, location='json')
        parser.add_argument('pickup', type=str, required=True, location='json')
        parser.add_argument('rider_id', required=True, type=int, location='json')
        parser.add_argument('amountpaid', required=True, type=float, location='json')
        parser.add_argument('ordereditems', type= list , required=True, help="This field is required", location='json')
        data = parser.parse_args()
        order = OrderModel(data['destination'],data['pickup'],user_id,data['rider_id'],data['amountpaid'])
         
         
        order.save_to_db()
        for  index in data['ordereditems']:
            item = ItemModel.find_by_name(index['name'])
            n_order = OrderItemModel(order.order_id,item.item_id,index['item_quantity'])
            n_order.save_to_db()
        return {"message": "Order was created successfully."}, 201



class OrderList(Resource):
    def get(self, user_id):
        return {'orders': list(map(lambda x: x.json(), OrderModel.query.filter_by(user_id=user_id)))}



class RiderEarnings(Resource):
    def get(self, username):
        totalearnings = 0
        orders = OrderModel.query.filter_by(rider_id = username)
        if orders:
            for order in orders:
                totalearnings =  totalearnings + order.amountpaid
            return totalearnings 
        return {"message": "order not found."}


            
class RiderRatings(Resource):
    def get(self, username):
        ratings = 0
        deliveries =DeliveryModel.query.filter_by(rider_username = username)
        count= deliveries.count()
        for delivery in deliveries:
            ratings =  ratings + delivery.delivery_feedback
        return ratings/count           

