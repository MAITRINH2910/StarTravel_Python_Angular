from flask import Blueprint, request, jsonify
from flask_bcrypt import Bcrypt
from app import db,bcrypt,app
from app.models.user_model import User
from app.models.hotel_model import Hotel
from app.api.user_api import token_required, token_required_role_admin, token_required_role_hotel_owner
import jwt
from functools import wraps
import os
import pickle
import numpy as np
from sqlalchemy import desc
import datetime
import config
import re
import json
import glob
import pandas as pd 

hotel_api = Blueprint('hotels', __name__, url_prefix='/hotels')

@hotel_api.route('/get_list_city',methods=['GET'])
def get_list_city():
    try:
        list_city = []
        files = os.listdir(config.PATH_MODEL_ML)
        for f in files:
            list_city.append(f.split(".")[0])
        return custom_response(list_city,200)
    except Exception as e:
        return custom_response(str(e),500)


def load_pickle(filename):
    with open(filename, 'rb') as handle:
        data = pickle.load(handle)
    return data

@hotel_api.route('/get_features',methods=['POST'])
def get_features():
    try:
        city = request.get_json()['city']
        filename = config.PATH_DATA + 'list_of_pro_hotel_'+ city +'.pickle'
        list_feature = load_pickle(filename)
        return custom_response(list_feature,200)
    except Exception as e:
        return custom_response(str(e),500)


def predict(city,rating,price,pro_predict,k = 20):
    with open(config.PATH_MODEL_ML+city+'.pickle', 'rb') as handle:
        clf = pickle.load(handle)
    with open(config.PATH_DATA+'list_of_pro_hotel_'+city+'.pickle', 'rb') as handle:
        list_of_pro = pickle.load(handle)
    
    X = [rating,int(price/config.UNIT_PRICE)]
    
    for i in range (5):
        X.append(X[1])

    for pro in list_of_pro:
        if pro in pro_predict:
            X.append(1)
        else:
            X.append(0)
    
    p = np.array(clf.decision_function([X]))

    ind = np.argpartition(p[0], -k)[-k:]

    y = []
    for i in ind:
        y.append((city+str(i)).replace(" ",""))
    return y

@hotel_api.route('/get_predicted_hotels',methods=['POST'])
def get_predicted_hotels():
    data = request.get_json()
    city = data['city']
    rating = data['rating']
    price = data['price']
    list_feature = data['list_feature']
    ids = predict(city,rating,price,list_feature)
    list_hotels = []
    try:
        for id in ids:
            hotel = Hotel.query.filter_by(id=id).first()
            if hotel is not None:
                list_hotels.append(hotel.dump())  
        return custom_response(list_hotels,200)
    except Exception as e:
        return custom_response({ 'error': str(e)},400)

@hotel_api.route('/get_top_hotels',methods=['POST'])
def get_top_hotels():
    data = request.get_json()
    city = data['city']
    hotels = Hotel.query.filter_by(city = city).filter_by(status="ACTIVE").order_by(desc(Hotel.rating))
    list_hotels = []
    count = 0
    try:
        for hotel in hotels:
            count +=1
            list_hotels.append(hotel.dump())
            if count == 10:
                break
        return custom_response(list_hotels,200)
    except Exception as e:
        return custom_response({ 'error': str(e)},400)

@hotel_api.route('/get_all_hotels_in_city/<string:city>', methods=['GET'])
def get_all_hotels_in_city(city):
    hotels = Hotel.query.filter_by(city=city,status='ACTIVE').all()
    listHotels = []
    for hotel in hotels:
        listHotels.append(hotel.dump())
    return custom_response(listHotels,200)

@hotel_api.route('/get_all_hotels_status/<string:status>', methods=['GET'])
@token_required_role_admin
def get_all_hotels_status(user,status):
    hotels = Hotel.query.filter_by(status=status).all()
    listHotels = []
    for hotel in hotels:
        listHotels.append(hotel.dump())
    return custom_response(listHotels,200)

@hotel_api.route('/get_all_hotels', methods=['GET'])
@token_required_role_admin
def get_all_hotels(user):
    hotels = Hotel.query.all()
    listHotels = []
    for hotel in hotels:
        listHotels.append(hotel.dump())
    return custom_response(listHotels,200)

@hotel_api.route('/get_all_hotels_of_owner', methods=['GET'])
@token_required_role_hotel_owner
def get_all_hotels_of_owner(current_user):
    hotels = Hotel.query.filter_by(hotel_owner_id=current_user.id).all()
    listHotels = []
    for hotel in hotels:
        listHotels.append(hotel.dump())
    return custom_response(listHotels,200)


@hotel_api.route('/get_one_hotel/<string:hotel_id>',methods=['GET'])
def get_one_hotel(hotel_id):
    res = [re.findall(r'(\w+?)(\d+)', hotel_id)[0]] 
    files = [f for f in glob.glob(config.PATH_DATA + "train/*.csv", recursive=True)]
    for f in files:
        if len(f.split("/")[-1].split(".")[0].split(" ")) > 2:
            city = f.split("/")[-1].split(".")[0].split(" ")[0] + f.split("/")[-1].split(".")[0].split(" ")[1] + f.split("/")[-1].split(".")[0].split(" ")[2]
        else:
            city = f.split("/")[-1].split(".")[0].split(" ")[0] + f.split("/")[-1].split(".")[0].split(" ")[1] 
        if res[0][0] == city:
            data = pd.read_csv(config.PATH_DATA + "train/" + str(f.split("/")[-1]))
            break
    
    hotel = Hotel.query.filter_by(id=hotel_id).first()
    if not hotel:
        return custom_response({'error' : 'No hotel found!'},404)
    dict_utilities = dict()
    if data[data["id"] == hotel_id].empty == False:
        for i , val in enumerate(data[data["id"] == hotel_id].columns):
            if i < 8:
                continue
            dict_utilities[str(data[data["id"] == hotel_id].columns[i])] = data[data["id"] == hotel_id].values[0][i]
    result = hotel.dump()
    return custom_response({"detail_hotels" : result , "utilities" : dict_utilities},200)

@hotel_api.route('/get_hotel_by_name',methods=['POST'])
def get_hotel_by_name():
    data = request.get_json()
    name = data['name']
    search = "%{}%".format(name)
    hotels = Hotel.query.filter_by(status="ACTIVE").filter(Hotel.name.like(search)).all()
    if not hotels:
        return custom_response({'error' : 'No hotel found!'},404)
    listHotels = []
    for hotel in hotels:
        listHotels.append(hotel.dump())
    return custom_response(listHotels,200)

@hotel_api.route('/add_hotel', methods=['POST'])
@token_required_role_hotel_owner
def add_hotel(current_user):
    data = request.get_json()
    hotel_id = data['city'].replace(" ","") + str(current_user.id) + str(int(datetime.datetime.now().timestamp()))  
    hotel_owner_id = current_user.id
    status = "INACTIVE"
    city = data['city']
    name = data['name']
    link = data['link']
    img = data['img']
    address = data['address']
    rating = float(data['rating'])
    price = int(data['price'])
    try:
        new_hotel = Hotel(hotel_id,hotel_owner_id,status,city,name,link,img,address,rating,price)
        db.session.add(new_hotel)
        db.session.commit()
        return custom_response({"success" : "Add hotel has been completed!"},200)
    except Exception as e:
        return custom_response({ 'error': "Duplicate address"},400)

@hotel_api.route('/approve_hotel/<string:hotel_id>',methods=['PUT'])
@token_required_role_admin
def approve_hotel(current_user,hotel_id):
    hotel = Hotel.query.filter_by(id=hotel_id).first()
    if not hotel:
        return custom_response({'error' : 'No hotel founded!'},404)
    if hotel.status == "ACTIVE":
        return custom_response({'error' : 'The hotel is in active state!'},400)
    hotel.status = "ACTIVE"
    db.session.commit()
    return custom_response({'success' : 'The hotel has been approved!'},200)

@hotel_api.route('/update_hotel/<string:hotel_id>',methods=['PUT'])
@token_required_role_hotel_owner
def update_hotel(current_user,hotel_id):
    data = request.get_json()
    hotel = Hotel.query.filter_by(id=hotel_id,hotel_owner_id=current_user.id).first()
    if not hotel:
        return custom_response({'error' : 'No hotel founded!'},404)
    hotel.status = 'INACTIVE'#data['status']
    hotel.city = data['city']
    hotel.name = data['name']
    hotel.link = data['link']
    hotel.img = data['img']
    hotel.address = data['address']
    hotel.rating = data['rating']
    hotel.price = data['price']
    try:
        db.session.commit()
        return custom_response({'success' : 'Update hotel has been completed!'},200)
    except Exception as e:
        return custom_response({ 'error': "Duplicate address"},400)



@hotel_api.route('/get_information_database',methods=['GET'])
@token_required_role_admin
def get_information_database(current_user):
    hotel = Hotel.query.count()
    user = User.query.count()
    hotel_active = Hotel.query.filter_by(status="ACTIVE").count()
    hotel_inactive = Hotel.query.filter_by(status="INACTIVE").count()
    result = {
        "number_of_hotel" :  hotel,
        "number_of_user" : user,
        "number_of_hotel_active" : hotel_active,
        "number_of_hotel_inactive" : hotel_inactive
    }
    return custom_response(result,200)

@hotel_api.route('/get_information_owner',methods=['GET'])
@token_required_role_hotel_owner
def get_information_owner(current_user):
    hotel = Hotel.query.filter_by(hotel_owner_id=current_user.id).count()
    hotel_active = Hotel.query.filter_by(hotel_owner_id=current_user.id).filter_by(status="ACTIVE").count()
    hotel_inactive = Hotel.query.filter_by(hotel_owner_id=current_user.id).filter_by(status="INACTIVE").count()
    result = {
        "number_of_hotel" :  hotel,
        "number_of_hotel_active" : hotel_active,
        "number_of_hotel_inactive" : hotel_inactive
    }
    return custom_response(result,200)

@hotel_api.route('/delete_hotel/<string:hotel_id>' , methods=['DELETE'])
@token_required_role_hotel_owner
def delete_hotel(current_user,hotel_id):
    try:
        hotel = Hotel.query.filter_by(id=hotel_id,hotel_owner_id=current_user.id).first()
        if not hotel:
            return custom_response({'error' : 'No hotel founded!'},404)
        db.session.delete(hotel)
        db.session.commit()
        return custom_response({'success' : 'Delete hotel has been completed!'},200)
    except Exception as e:
        return custom_response({"error" : str(e) } ,400)


@hotel_api.route('/update/<string:hotel_id>',methods=['PUT'])
@token_required_role_admin
def update(current_user,hotel_id):
    data = request.get_json()
    hotel = Hotel.query.filter_by(id=hotel_id).first()
    if not hotel:
        return custom_response({'error' : 'No hotel founded!'},404)
    hotel.status = data['status']
    hotel.city = data['city']
    hotel.name = data['name']
    hotel.link = data['link']
    hotel.img = data['img']
    hotel.address = data['address']
    hotel.rating = data['rating']
    hotel.price = data['price']
    try:
        db.session.commit()
        return custom_response({'success' : 'Update hotel has been completed!'},200)
    except Exception as e:
        return custom_response({ 'error': "Duplicate address"},400)

@hotel_api.route('/delete/<string:hotel_id>' , methods=['DELETE'])
@token_required_role_admin
def delete(current_user,hotel_id):
    try:
        hotel = Hotel.query.filter_by(id=hotel_id).first()
        if not hotel:
            return custom_response({'error' : 'No hotel founded!'},404)
        db.session.delete(hotel)
        db.session.commit()
        return custom_response({'success' : 'Delete hotel has been completed!'},200)
    except Exception as e:
        return custom_response({"error" : str(e) } ,400)

def custom_response(res, status_code):
  """
  Custom Response Function
  """
  return jsonify(
    mimetype="application/json",
    response=res,
    status=status_code
  )
