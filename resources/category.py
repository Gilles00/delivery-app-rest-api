# __author__ = "Kimberly"


from flask_restful import Resource, Api, abort, reqparse
from models.categoryModel import CategoryModel
from models.itemModel import ItemModel
from flask import jsonify
from flask import request
from db import db


class Category(Resource):
    def get(self, category_id):
        querie = CategoryModel.query.get(category_id)

        if querie is None:
            return jsonify(
                {'error': "Category Not Found"}
            )
        else:
            return jsonify({
                'category_id': querie.category_id,
                'category_name': querie.category_name
            })

    def post(self):
        json_data = request.get_json(force=True)

        if json_data is None:
            return jsonify(
                {'error': "No data was inserted"}
            )

        data = CategoryModel(cat_name=json_data['category_name'])
                         
        db.session.add(data)
        db.session.commit()
        return jsonify({'message': 'New category successfully added'})

    def delete(self, category_id):
        data = CategoryModel.query.get(category_id)

        if data is None:
            return jsonify(
                {'error': "Category Not Found"})
        
        db.session.delete(data)
        db.session.commit()
        return jsonify(
            {'message': "Category was successfully deleted"}
        )

class AllCategories(Resource):
        def get(self):
            return {'categories': list(map(lambda x: x.json(), CategoryModel.query.all()))}

class CategoryItems(Resource):
        def get(self, category_id):
            array =[]
            itemObjects = ItemModel.query.filter_by(category_id=category_id).paginate(page=1, per_page = 5)
            items = itemObjects.items
            for x in range (len(items)):
                 item = items[x]
                 ob = {
                     "item_id": item.item_id,
                     "item_name": item.item_name,
                     "unit_price": item.unit_price
                     }
                 array.append(ob)
            return array            

    
               