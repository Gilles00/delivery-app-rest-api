# __author__ = "sarkodie"


from db import db
from authentication import create_password_hash
    
class RiderModel(db.Model):
    __tablename__= 'rider'
    
    rider_id = db.Column(db.Integer, primary_key=True)
    rider_firstname = db.Column(db.String(50), nullable=False)
    rider_lastname = db.Column(db.String(50), nullable=False)
    rider_username = db.Column(db.String(50), index =True, nullable =False, unique =True)
    rider_email = db.Column(db.String(120), index=True, nullable=False, unique=True)
    password = db.Column(db.Binary(120), nullable=False)
    rider_nationality = db.Column(db.String(50), index=True, nullable=False)  
    rider_dateofbirth = db.Column(db.String(15), nullable=False)
    rider_profilepicture = db.Column(db.String(450),index=True, nullable=False,unique=True)
    rider_gender = db.Column(db.String(1),nullable=False)
    salt = db.Column(db.Binary(50),nullable=False)
    status = db.Column(db.Integer, default= 0)
    lon = db.Column(db.Float(precision=4), nullable= True, default =0.00)
    lat = db.Column(db.Float(precision=4), nullable= True, default = 0.00)
    #earnings = db.Column(db.Decimal(10,2), nullable=True, default=0.0)
    #ratings = db.Column(db.dec(200), nullable=True , default ='0')

    account = db.relationship('AccountModel')
    vehicle = db.relationship('VehicleModel')

    
    def __init__(self, rider_firstname, rider_lastname, rider_username, rider_email, rider_password, rider_nationality, rider_dateofbirth, rider_profilepicture,rider_gender):
        self.rider_firstname = rider_firstname
        self.rider_lastname = rider_lastname
        self.rider_username = rider_username
        self.rider_email = rider_email
        self.rider_nationality = rider_nationality
        self.rider_dateofbirth = rider_dateofbirth
        self.rider_profilepicture = rider_profilepicture
        self.rider_gender = rider_gender
        self.password,self.salt = create_password_hash(rider_password)
        #self.earnings = totalearnings(rider)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_rider_id(cls, rider_id):
        return cls.query.filter_by(rider_id = rider_id).first()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(rider_username=username).first()
   
    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(rider_email=email).first()

    @classmethod
    def find_by_picture(cls, picture):
        return cls.query.filter_by(rider_profilepicture=picture).first()

    @classmethod
    def find_by_status(cls, status):
        return cls.query.filter_by(status = status).all()
    
    @property
    def is_active(self):
        """Always True, as all users are active."""
        return True

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()