# __author__ = "Crhistian Barnes "


from flask_restful import Resource, reqparse
from sqlalchemy.exc import SQLAlchemyError
from models.itemModel import ItemModel
from db import db
from models.shopModel import ShopModel
from flask import jsonify
from models.categoryModel import CategoryModel

#Manually declaring a paginate function to take care of pagination of item models
def paginate(total, per_page=5):
    paginateItems = []
    m = per_page-1
    for x in range (0, m):
        paginateItems.append(total[x])
    return paginateItems



class Item(Resource):
    def get(self,item_name):        
        item = ItemModel.find_by_name(item_name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    def post(self,item_name):
        parser = reqparse.RequestParser()
        parser.add_argument('price', type=float, required=True, location='json')
        parser.add_argument('category', type=str, required=True, location='json')
        data = parser.parse_args()
        holder = CategoryModel.find_by_category_name(data['category'])
        if holder:
            item = ItemModel(item_name,data['price'],holder.category_id)
            item.save_to_db() 
            return {"message":"item successfully added"}
        return {"message":"category not recogonzied"}
  

class ItemList(Resource):
    def get(self):
        return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}


class ShopItems(Resource):
    def post(self, shop_id):
        array = []
        data = ShopModel.query.get(shop_id)
        for x in range (len(data.items)):
            item = data.items[x]
            ob = {
                "item_id": item.item_id,
                "item_name": item.item_name,
                "unit_price": item.unit_price
            }
            array.append(ob)
        return paginate(array)  
            
# class ItemPrice(Resource):
#     def get(self):
#         parser = reqparse.RequestParser()
#         parser.add_argument('price', type=float, required=True, location='json')
#         return {'items': list(map(lambda x: x.json(), ItemModel.query.(where price <= data))}