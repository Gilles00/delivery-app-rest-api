# __author__ = "sarkodie"


from db import db
from authentication import create_password_hash
    
class AdminModel(db.Model):
    __tablename__= 'admin'
    
    admin_id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), index =True, nullable =False, unique =True)
    email = db.Column(db.String(120), index=True, nullable=False, unique=True)
    password = db.Column(db.Binary(120), nullable=False)
    nationality = db.Column(db.String(50), index=True, nullable=False, unique=True)
    salt = db.Column(db.Binary(50),nullable=False)

    def __init__(self, firstname, lastname, username, email, nationality, password):
        self.firstname = firstname
        self.lastname = lastname
        self.username = username
        self.email = email
        self.nationality = nationality
        self.password,self.salt = create_password_hash(password)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

        
    @classmethod
    def find_by_email(cls, mail):
        return cls.query.filter_by(email=mail).first()
        