# __author__ = "Crhistian Barnes "


from db import db
from models.categoryModel import CategoryModel


class ItemModel(db.Model):
    __tablename__ = 'item'

    item_id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(80), nullable=False)
    unit_price = db.Column(db.Float(precision=2), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.category_id'), nullable=False)
      
    orderitem = db.relationship('OrderItemModel')
    

    def __init__(self, item_name, price, category_id):
        self.item_name = item_name
        self.unit_price = price
        self.category_id = category_id

    def json(self): 
        cat = CategoryModel.find_by_id(self.category_id)
        return {'name': self.item_name, 'price': self.unit_price, 'category': cat.category_name}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(item_name =name).first()
    
    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(item_id =id).first()