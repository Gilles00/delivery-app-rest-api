# __author__ = "Crhistian Barnes "


from db import db  
from authentication import create_password_hash


class UserModel(db.Model):
    __tablename__= 'user'

    user_id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), index=True, nullable=False, unique=True)
    phonenumber = db.Column(db.String(20), index=True, nullable=False, unique=True)
    gender = db.Column(db.String(1),nullable=False)
    dateofbirth = db.Column(db.String(10), nullable=False)
    password = db.Column(db.Binary(120), nullable=False)
    username = db.Column(db.String(64), index=True, nullable=False, unique=True)
    location = db.Column(db.String(50), nullable=False)
    salt = db.Column(db.Binary(50),nullable=False)

    
    def __init__(self, firstname, lastname, email, phonenumber, gender, dateofbirth, password, username, location):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.phonenumber = phonenumber
        self.gender = gender
        self.dateofbirth = dateofbirth
        self.username = username
        self.location = location
        self.password,self.salt = create_password_hash(password)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, uid):
        return cls.query.filter_by(user_id=uid).first()
        
    @classmethod
    def find_by_email(cls, mail):
        return cls.query.filter_by(email=mail).first()
        
    @classmethod
    def find_by_phonenumber(cls, cell):
        return cls.query.filter_by(phonenumber=cell).first()