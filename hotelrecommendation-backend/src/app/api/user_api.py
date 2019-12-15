from flask import Blueprint, request, jsonify
from flask_bcrypt import Bcrypt
from app import db,bcrypt,app
from app.models.user_model import User
from app.models.hotel_model import Hotel
import jwt
from functools import wraps
import os
import pickle
import numpy as np
from sqlalchemy import desc
import datetime
import config
user_api = Blueprint('users', __name__, url_prefix='/users')


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'user-access-token' in request.headers:
            token = request.headers['user-access-token']

        if not token:
            return custom_response({'message' : 'Token is missing!'},401)

        try:
            data = jwt.decode(token, config.SECRET_KEY)
            current_user = User.query.filter_by(username=data['username']).first()
        except jwt.ExpiredSignatureError as e1:
            return custom_response({'message': 'token expired, please login again'},401)
        except:
            return custom_response({'message' : 'Token is invalid!'},401) 

        return f(current_user, *args, **kwargs)

    return decorated


def token_required_role_hotel_owner(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'user-access-token' in request.headers:
            token = request.headers['user-access-token']

        if not token:
            return custom_response({'message' : 'Token is missing!'},401)

        try:
            data = jwt.decode(token, config.SECRET_KEY)
            if data['role'] != "HOTEL_OWNER":
                return custom_response({'message' : 'Permission denied '},401)
            current_user = User.query.filter_by(username=data['username']).first()
        except jwt.ExpiredSignatureError as e1:
            return custom_response({'message': 'token expired, please login again'},401)
        except:
            return custom_response({'message' : 'Token is invalid!'},401) 

        return f(current_user, *args, **kwargs)

    return decorated


def token_required_role_admin(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'user-access-token' in request.headers:
            token = request.headers['user-access-token']

        if not token:
            return custom_response({'message' : 'Token is missing!'},401)

        try:
            data = jwt.decode(token, config.SECRET_KEY)
            if data['role'] != "ADMIN":
                return custom_response({'message' : 'Permission denied '},401)
            current_user = User.query.filter_by(username=data['username']).first()
        except jwt.ExpiredSignatureError as e1:
            return custom_response({'message': 'token expired, please login again'},401)
        except:
            return custom_response({'message' : 'Token is invalid!'},401) 

        return f(current_user, *args, **kwargs)

    return decorated


@user_api.route('/update_current_user',methods=['PUT'])
@token_required
def update_current_user(current_user):
    data = request.get_json()
    current_user.password = bcrypt.generate_password_hash(
        data['password']).decode('utf-8')
    db.session.commit()
    return custom_response({'success' : 'Update user has been completed!'},200)

@user_api.route('/get_all_user',methods=['GET'])
@token_required_role_admin
def get_all_user(current_user):
    users = User.query.all()
    listUsers = []
    for user in users:
        listUsers.append(user.dump())
    return custom_response(listUsers,200)


@user_api.route('/get_information_current_user',methods=['GET'])
@token_required
def get_information_current_user(current_user):

    result = {
        "id" : current_user.id,
        "username" : current_user.username,
        "role" : current_user.role
    }
    return custom_response(result,200)

@user_api.route('/register', methods=['POST'])
def register():
    try:
        list_role = ["ADMIN","HOTEL_OWNER","USER"]
        username = request.get_json()['username']
        password = bcrypt.generate_password_hash(
            request.get_json()['password']).decode('utf-8')
        role = request.get_json()['role']
        if role not in list_role:
            return custom_response({"error" : "Invalid role"}, 400)
        newuser = User(username,password,role)
        user = User.get_user_by_username(username)
        if(user != None):
            return custom_response({"error" : "Duplicate username"}, 400)
        else:
            db.session.add(newuser)
            db.session.commit()
            result = newuser.dump()
        return custom_response(result,200)
    except Exception as e:
        return custom_response({"error" : str(e)}, 400)

@user_api.route('/login', methods=['POST'])
def login():
    try:
        username = request.get_json()['username']
        password = request.get_json()['password']
        result = ''
        if not username or not password:
            return custom_response({'error': 'you need username and password to sign in'}, 400)
        user = User.get_user_by_username(username)
        if user != None:
            if bcrypt.check_password_hash(user.password, password):
                access_token = jwt.encode({
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
                    'iat': datetime.datetime.utcnow(),
                    'sub': user.id,
                    'username': user.username,
                    'role' : user.role
                }, config.SECRET_KEY)
                result = access_token.decode("utf-8")
            else:
                return custom_response({"error": "Invalid username or password!"},400)
        else:
            return custom_response({"error": "Invalid username or password!"},400)
        return custom_response({'token' : result , 'role' : user.role,'username' : user.username},200)
    except Exception as e:
        return custom_response({"error" : str(e)}, 400)


@user_api.route('/delete_user/<string:user_id>' , methods=['DELETE'])
@token_required_role_admin
def delete_hotel(current_user,user_id):
    try:
        user_id = int(user_id)
        user = User.query.filter_by(id=user_id).first()
        if user.role == "ADMIN":
            return custom_response({'error' : 'Permission denied!'},400)
        if not user:
            return custom_response({'error' : 'No user founded!'},404)
        db.session.delete(user)
        db.session.commit()
        return custom_response({'success' : 'Delete user has been completed!'},200)
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
