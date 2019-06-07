# __author__ = "sarkodie"


from db import db


class AccountModel(db.Model):
    __tablename__ = 'rider_bank_account'

    rider_account_number = db.Column(db.String(85), nullable = False,unique=True,primary_key=True)   # should all riders have a bank account?
    rider_holdername = db.Column(db.String(120), nullable = False)      # and if no then nullable can be true
    
    rider_id = db.Column(db.Integer, db.ForeignKey('rider.rider_id'),nullable=False)
    rider = db.relationship('RiderModel')

    def __init__(self, rider_account_number, rider_holdername, rider_id):
        self.rider_account_number = rider_account_number
        self.rider_holdername = rider_holdername
        self.rider_id = rider_id

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    @classmethod
    def find_by_holdername(cls, name):
        return cls.query.filter_by(rider_holdername = name).first()

    @classmethod
    def find_by_rider_account_number(cls, name):
        return cls.query.filter_by(rider_account_number = name).first()