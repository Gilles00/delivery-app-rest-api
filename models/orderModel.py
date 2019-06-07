# __author__ = "Crhistian Barnes "


from db import db
from models.userModel import UserModel
from models.riderModel import RiderModel
from models.orderItemModel import OrderItemModel
from models.itemModel import ItemModel
from sqlalchemy.sql import func

class OrderModel(db.Model):
    __tablename__ = "order"

    order_id = db.Column(db.Integer, primary_key=True)
    destination = db.Column(db.String(50), nullable=False)
    ordertime =  db.Column(db.DateTime, nullable=False, default=func.now())
    pickup_point = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    rider_id = db.Column(db.Integer, db.ForeignKey('rider.rider_id'), nullable=False)
    amountpaid = db.Column(db.Float, nullable=False)
    
    delivery = db.relationship('DeliveryModel')
    orderitem = db.relationship('OrderItemModel')
     
    def __init__(self, destination, pickup, user_id, rider_id, amountpaid):
        self.destination = destination
        self.pickup_point = pickup
        self.user_id = user_id
        self.rider_id = rider_id
        self.amountpaid = amountpaid

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()


    @classmethod
    def find_by_id(cls, oid):
        return cls.query.filter_by(user_id=oid).first()
    
    @classmethod
    def find_by_riderid(cls, rid):
        return cls.query.filter_by(rider_id=rid).last()
    
    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(rider_username=username).first()

    def json(self):
        user = UserModel.find_by_id(self.user_id)
        rider = RiderModel.find_by_rider_id(self.rider_id)
        ridername =  rider.rider_firstname+' '+rider.rider_lastname
        overitems =  OrderItemModel.find_by_orderid(self.order_id)
        orderitems =[]
        for order in overitems:
            item  = ItemModel.find_by_id(order.item_id)
            orderitems.append(dict({"item_name":item.item_name,"item price":item.unit_price,"quantity":order.item_quantity}))
        return {"username":user.username, "Ridername": ridername, "destination":self.destination,
                 'pickup':self.pickup_point, 'ordertime':str(self.ordertime), 'amountpaid':self.amountpaid,
                 "ordererditems":orderitems}
