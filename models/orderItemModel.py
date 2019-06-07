# __author__ = "Crhistian Barnes "


from db import db

class OrderItemModel(db.Model):
    __tablename__ = "orderitem"
    
    oi_id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.order_id'))
    item_id = db.Column(db.Integer, db.ForeignKey('item.item_id'),nullable=False)
    item_quantity = db.Column(db.Integer,nullable=False)

    order = db.relationship('OrderModel')
    item = db.relationship('ItemModel')

    def __init__(self, order_id, item_id, item_quantity):
        self.order_id = order_id
        self.item_id = item_id
        self.item_quantity = item_quantity
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    
    @classmethod
    def find_by_orderid(cls, orid):
        return cls.query.filter_by(order_id=orid)