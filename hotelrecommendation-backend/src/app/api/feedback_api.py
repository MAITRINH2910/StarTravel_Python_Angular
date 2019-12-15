from flask import Blueprint, request, jsonify
from flask_bcrypt import Bcrypt
from app import db,bcrypt,app
from app.models.user_model import User
from app.models.hotel_model import Hotel
from app.models.feedback_model import Feedback
import jwt
from functools import wraps
import config
import json
from app.api.user_api import token_required, token_required_role_admin, token_required_role_hotel_owner

feedback_api = Blueprint('feedback', __name__, url_prefix='/feedback')


@feedback_api.route('/get_all',methods=['GET'])
@token_required_role_admin
def get_all_feedback(user):
    try:
        feedbacks = Feedback.get_all_feedback()
        result = []
        for fb in feedbacks:
            result.append(fb.dump())
        return custom_response(result,200)
    except Exception as e:
        return custom_response(str(e),500)


@feedback_api.route('/get/<string:hotel_id>',methods=['GET'])
def get_feedback_of_hotel(hotel_id):
    try:
        feedbacks = Feedback.get_feedback_by_hotel_id(hotel_id)
        result = []
        for fb in feedbacks:
            result.append(fb[0].dump(fb[1]))
        return custom_response(result,200)
    except Exception as e:
        return custom_response(str(e),500)


@feedback_api.route('/add', methods=['POST'])
@token_required
def add_feedback(current_user):
    try:
        data = request.get_json()
        hotel_id = data['hotel_id']
        user_id = current_user.id
        content = data['content']
        rating = data['rating']
        new_feedback = Feedback(user_id,hotel_id,content,rating)
        db.session.add(new_feedback)
        db.session.commit()
        # result = new_feedback.dump()
        return custom_response('added',200)
    except Exception as e:
        return custom_response(str(e),500)

@feedback_api.route('/delete/<int:id>' , methods=['DELETE'])
@token_required_role_admin
def delete_feedback(current_user,id):
    try:
        feedback = Feedback.query.filter_by(id=id).first()
        if not feedback:
            return custom_response({'message' : 'No feedback found!'},404)
        db.session.delete(feedback)
        db.session.commit()
        return custom_response({'message' : 'Delete feedback has been completed!'},200)
    except Exception as e:
        return custom_response({"message" : str(e) } ,400)

# @feedback_api.route('/update/<int:id>' , methods=['POST'])
# @token_required_role_admin
# def update_feedback(current_user,id):
#     try:
#         feedback = Feedback.query.filter_by(id=id).first()
#         if not feedback:
#             return custom_response({'message' : 'No feedback found!'},404)
#         db.session.delete(feedback)
#         db.session.commit()
#         return custom_response({'message' : 'Delete feedback has been completed!'},200)
#     except Exception as e:
#         return custom_response({"message" : str(e) } ,400)



def custom_response(res, status_code):
  """
  Custom Response Function
  """
  return jsonify(
    mimetype="application/json",
    response=res,
    status=status_code
  )
