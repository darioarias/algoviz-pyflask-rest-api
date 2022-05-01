from . import api_v1
from flask import jsonify, request, json, g, url_for, redirect, request
from .route_controls import abort_request, query_chain
from app.models import User
from app import db
from sqlalchemy.exc import IntegrityError
from app.email import send_email
from flask_jwt_extended import jwt_required

# Create
@api_v1.route('/users/', methods=['POST'])
@jwt_required()
def create_user():
  if 'password' in request.json:
    request.json['password'] = User.generate_hash(request.json['password'])

  user = User(
    username=request.json.get('username', None),
    email=request.json.get('email', None),
    password=request.json.get('password', None),
    first_name=request.json.get('first_name', None),
    last_name=request.json.get('last_name', None)
  )
  
  try:
    db.session.add(user)
    db.session.commit()
    send_email(
      user.email, 
      'Confirm Account', 
      'email/confirm', 
      user=user, 
      token=user.generate_verification_token(user.username)
    )
  except IntegrityError as error:
    abort_request(message="Unable to create User", code=500, details=error.orig.diag.message_detail)
  finally:
    db.session.rollback()
  return redirect(url_for('api_v1.read_user', id=user.id))

# Read
@api_v1.route('/users/', methods=['GET'])

def read_users():
  users = query_chain(Model = User)
  users_list = []
  for user in users:
    users_list.append(user.to_json())
  return jsonify(users_list)

@api_v1.route('/users/<int:id>', methods=['GET'])
def read_user(id):
  user = query_chain(Model=User, PK_key=id).first_or_404()
  # TESTING EMAIL SENDING
  # send_email('pepelope8@gmail.com', 'Confirm account', 'email/confirm', user=user, token='someHash')
  
  t = User.find_by_username('d_arias')
  print(t.password if t is not None else " method not working")

  # END TEST
  return jsonify([user.to_json()])

# Update
@api_v1.route('/users/<int:id>', methods=["PUT", "PATCH"])
@jwt_required()
def update_user(id):
  user = query_chain(Model=User, PK_key=id).first()
  code = 200
  if request.method == "PUT":
    if user is None:
      user = User(
        username=request.json.get('username', None), 
        email=request.json.get('email', None), 
        password=request.json.get('password', None),
        first_name=request.json.get('first_name', None),
        last_name=request.json.get('last_name', None),
      )
      code = 201
      db.session.add(user)
    else:
      user.username = request.json.get('username', None)
      user.email = request.json.get('email', None)
      user.password = request.json.get('password', None)
      user.first_name = request.json.get('first_name', None)
      user.last_name = request.json.get('last_name', None)

  if request.method == "PATCH":
    if user is None:
      abort_request(message="User does not exits", code=400)
    
    user.username = request.json.get('username', user.username)
    user.email = request.json.get('email', user.email)
    user.password = request.json.get('password', user.password)
    user.first_name = request.json.get('first_name', user.first_name)
    user.last_name = request.json.get('last_name', user.last_name)

  try:
    db.session.commit()
  except IntegrityError as error:
    abort_request('Unable to update user', details=error.orig.diag.message_detail)
  finally:
    db.session.rollback()
  return redirect(url_for('api_v1.read_user', id=user.id), code=code)

# Delete
@api_v1.route('/users/<int:id>', methods=["DELETE"])
@jwt_required()
def delete_user(id):
  user = query_chain(Model=User, PK_key=id).first()
  if user is None:
    abort_request(message="User does not exits", code=400)
  
  try:
    db.session.delete(user)
    db.session.commit()
  except IntegrityError as error:
    abort_request('Unable to delete user', code=500, details=error.orig.diag.message_detail)
  finally:
    db.session.rollback();

  # return redirect(url_for('api_v1.read_users'))
  return jsonify({'message': "user deleted"})
