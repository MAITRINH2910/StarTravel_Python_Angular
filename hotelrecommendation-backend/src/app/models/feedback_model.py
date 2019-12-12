from app import db,bcrypt
from flask_bcrypt import Bcrypt
from app.models.user_model import User

# Define a base model for other database tables to inherit
class Base(db.Model):

    __abstract__  = True

    id = db.Column(db.Integer, db.Sequence('users_id_seq'), primary_key=True)
    # created  = db.Column(db.DateTime,  default=db.func.current_timestamp())
    # modified  = db.Column(db.DateTime,  default=db.func.current_timestamp())

# Define a User model
class Feedback(Base):
    __tablename__ = 'feedback'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'),nullable=False)
    # users = db.relationship("User", backref=db.backref("users", uselist=False))
    hotel_id = db.Column(db.Text, db.ForeignKey('hotels.id'),nullable=False)
    # hotels = db.relationship("Hotel", backref=db.backref("hotels", uselist=False))
    content = db.Column(db.Text,nullable=False)
    rating = db.Column(db.Float,nullable=False)

    def __init__(self,user_id,hotel_id,content,rating):
        self.user_id = user_id
        self.hotel_id = hotel_id
        self.rating = rating
        self.content = content

    @staticmethod
    def get_all_feedback():
        return Feedback.query.all()

    @staticmethod
    def get_one_feedback(id):
        return Feedback.query.get(id)

    @staticmethod
    def get_feedback_by_hotel_id(hotel_id):
        #return Feedback.query.filter_by(hotel_id=value)
        return Feedback.query.join(User, User.id==Feedback.user_id).add_columns(User.username).filter(Feedback.hotel_id == hotel_id).all()
        
    def __repr__(self):
        return '<id {}>'.format(self.id)

    def dump(self,username=''):
        feedback = dict()
        feedback['id'] = self.id
        feedback['user_id'] = self.user_id
        feedback['hotel_id'] = self.hotel_id
        feedback['content'] = self.content
        feedback['rating'] = self.rating
        feedback['username'] = username
        return feedback

