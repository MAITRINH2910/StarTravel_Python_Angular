from app import db,bcrypt
from flask_bcrypt import Bcrypt
# Define a base model for other database tables to inherit
class Base(db.Model):

    __abstract__  = True

    id = db.Column(db.Integer, db.Sequence('users_id_seq'), primary_key=True)
    # created  = db.Column(db.DateTime,  default=db.func.current_timestamp())

class User(Base):

    __tablename__ = 'users'
    username    = db.Column(db.String(128),  nullable=False,
                                            unique=True)
    password    = db.Column(db.String(192),  nullable=False)
    role    = db.Column(db.String(10),  nullable=False)    
    # New instance instantiation procedure
    def __init__(self,username,password,role):
        self.username    = username
        self.password = password
        self.role = role

    @staticmethod
    def get_all_users():
        return User.query.all()

    @staticmethod
    def get_one_user(id):
        return User.query.get(id)

    @staticmethod
    def get_user_by_username(value):
        return User.query.filter_by(username=value).first()
        
    def __repr__(self):
        return '<id {}>'.format(self.id)

    def dump(self):
        user = {
                'id': self.id,
                'username': self.username,
                'role': self.role
            }
        return user
