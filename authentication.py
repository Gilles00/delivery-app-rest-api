# __author__ = "Crhistian Barnes "

import bcrypt

def create_password_hash(password):
    salt = bcrypt.gensalt(16)
    hashed_pass = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_pass,salt

def check_password(password,user): 
    if user.salt is not None:
        generated_hash = recreate_hash(password.encode('utf-8'),user.salt)
        return (user.password == generated_hash)
    return False

def recreate_hash(password, salt):
    hash_pass = bcrypt.hashpw(password, salt)
    return hash_pass
