# __author__ = "sarkodie"


from flask_restful import Resource, fields, reqparse, request
from sqlalchemy.exc import SQLAlchemyError
from models.riderBankAccountModel import AccountModel


class vehicle(Resource):   ## fetching a registered account given a holdername. 
    def get(self, rider_holdername):
        AccountModel.find_by_holdername(rider_holdername)
  

class Account_List(Resource): ## displaying a list of all registered accounts
    def get(self):
        return {'items': list(map(lambda x: x.json(), AccountModel.query.all()))}
