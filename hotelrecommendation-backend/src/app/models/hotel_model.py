from app import db,bcrypt
from flask_bcrypt import Bcrypt
# Define a base model for other database tables to inherit
class Base(db.Model):

    __abstract__  = True

    id = db.Column(db.Text, primary_key=True)
    # created  = db.Column(db.DateTime,  default=db.func.current_timestamp())
    # modified  = db.Column(db.DateTime,  default=db.func.current_timestamp())

# Define a User model
class Hotel(Base):
    __tablename__ = 'hotels'
    hotel_owner_id = db.Column(db.Integer, db.ForeignKey('users.id'),nullable=False)
    users = db.relationship("User", backref=db.backref("users", uselist=False))
    status = db.Column(db.Text,nullable=False)
    city = db.Column(db.Text,nullable=False)
    name = db.Column(db.Text,nullable=False)
    link = db.Column(db.Text,nullable=True)
    img = db.Column(db.Text,nullable=True)
    address = db.Column(db.Text,nullable=False)
    rating = db.Column(db.Float,nullable=False)
    price = db.Column(db.Integer,nullable=False)

    def __init__(self,hotel_id,hotel_owner_id,status,city,name,link,img,address,rating,price):
        self.id = hotel_id
        self.hotel_owner_id = hotel_owner_id
        self.status = status
        self.city = city
        self.name = name
        self.link = link
        self.img = img
        self.address = address
        self.rating = rating
        self.price = price

    def __repr__(self):
        return '<Hotel %r>' % (self.name)

    def dump(self):
        hotel = dict()
        hotel['id'] = self.id
        hotel['hotel_owner'] = self.users.username
        hotel['status'] = self.status
        hotel['city'] = self.city
        hotel['name'] = self.name
        hotel['link'] = self.link
        hotel['img'] = self.img
        hotel['address'] = self.address
        hotel['rating'] = self.rating
        hotel['price'] = self.price
        return hotel
