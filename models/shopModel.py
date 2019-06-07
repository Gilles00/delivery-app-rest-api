# __author__ = "Kimberly"


from db import db
from sqlalchemy import Table, Column, Integer, ForeignKey

#Bridge Table
shop_has_items = db.Table('shop_has_items', db.Model.metadata,
                            db.Column('shop_id', db.Integer, db.ForeignKey('shop.shop_id'), primary_key=True),
                            db.Column( 'item_id', db.Integer, db.ForeignKey('item.item_id'), primary_key=True))
    


class ShopModel(db.Model):
    __tablename__ = 'shop'

    shop_id = db.Column(db.Integer, primary_key=True)
    shop_name = db.Column(db.String(45), nullable=False)
    shop_location = db.Column(db.String(45), nullable=False)
    shop_coordinates = db.Column(db.String(45), nullable=False)
    shop_description = db.Column(db.String(250), nullable=False)
    
    items = db.relationship('ItemModel', secondary=shop_has_items)
    
    def __init__(self, name, location, coordinates, description):
        self.shop_name = name
        self.shop_location = location
        self.shop_coordinates = coordinates
        self.shop_description = description

    def json(self): 
        return {'id': self.shop_id, 'shop': self.shop_name, 'location': self.shop_location, 'coordinates': self.shop_coordinates, 'description': self.shop_description}

    @classmethod
    def find_by_name(cls, shop):
        return cls.query.filter_by(shop_name=shop).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()    

