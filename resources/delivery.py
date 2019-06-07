# __author__ = "Kimberly"


from flask_restful import Resource, Api, abort, reqparse
from models.deliveryModel import DeliveryModel
from flask import jsonify
from db import db
from flask import request


class Delivery(Resource):
    def get(self, delivery_id):
        querie = DeliveryModel.query.get(delivery_id)

        if querie is None:
            return jsonify(
                {'error': " Not Found"}
            )
        else:
            return jsonify({
                'delivery_id': querie.delivery_id,
                'delivery_status': querie.delivery_status,
                'delivery_duration': str((querie.delivery_duration)),
                'order_id': querie.order_id
            })

    def post(self):
        json_data = request.get_json(force=True)

        if json_data is None:
            return jsonify(
                {'error': "No data was inserted"}
            )

        data = DeliveryModel(staus=json_data['delivery_status'],
                             duration=json_data['delivery_duration'],
                             order=json_data['order_id'])
        db.session.add(data)
        db.session.commit()
        return jsonify({'message': 'New delivery successfully inserted'})

    def delete(self, delivery_id):
        data = DeliveryModel.query.get(delivery_id)

        if data is None:
            return jsonify(
                {'error': "Delivery Not Found"})
        
        db.session.delete(data)
        db.session.commit()
        return jsonify(
            {'message': "Delivery Information was successfully deleted"}
        )

            
        
        
    