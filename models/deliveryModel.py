# __author__ = "Kimberly "


from db import db
from sqlalchemy import Table, Column, Integer, ForeignKey


class DeliveryModel(db.Model):
    __tablename__ = 'delivery'

    delivery_id = db.Column(db.Integer, primary_key=True)
    delivery_status = db.Column(db.Boolean)
    delivery_duration = db.Column(db.DateTime)
    delivery_feedback = db.Column(db.String(200))
    order_id = db.Column(db.Integer, db.ForeignKey('order.order_id'), nullable= False)

    
    order = db.relationship('OrderModel')
    
    def __init__(self, status, duration, order, feedback):
        self.delivery_status = status
        self.delivery_duration = duration
        self.order_id = order
        self.delivery_feedback = feedback
    
    

