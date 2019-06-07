# __author__ = "Kimberly "


from db import db
from sqlalchemy import Table, Column, Integer, ForeignKey


class CategoryModel(db.Model):
    __tablename__ = 'category'
 
    category_id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(45), nullable=False)
    items = db.relationship('ItemModel', backref='categories')


    def __init__(self,  cat_name):
        self.category_name = cat_name

    def json(self): 
        return {'id': self.category_id, 'category': self.category_name}

   
    @classmethod
    def find_by_category_name(cls, cat_name):
        return cls.query.filter_by(category_name=cat_name).first()
    
    @classmethod
    def find_by_id(cls, cat_id):
        return cls.query.filter_by(category_id=cat_id).first()

