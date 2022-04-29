from . import api
from flask import jsonify, request, json, g, url_for, redirect, request
from .route_controls import abort_request
from app.models import User
from app import db
from sqlalchemy.exc import IntegrityError

#TODO: Abstract this logic into module
def query_chain(Model, PK_key: int = None, Count: int = None):
  if(Model is None):
    raise Exception('Model must be provided')

  query = db.session.query(Model)

  if PK_key is not None:
    query = query.filter(Model.id == PK_key)
  
  if Count is not None:
    query = query.limit(Count)
  
  return query

# Create
@api.route('/users/', methods=['POST'])
def create_user():
  user = User(
    username=request.json.get('username' or ''), 
    email=request.json.get('email' or ''), 
    password=request.json.get('password' or ''),
    first_name=request.json.get('first_name' or ''),
    last_name=request.json.get('last_name' or ''),
  )
  try:
    db.session.add(user)
    db.session.commit()
  except IntegrityError as error:
    abort_request(message="Unable to create User", code=500, details=error.orig.diag.message_detail)
  finally:
    db.session.rollback()
  return redirect(url_for('api.read_user', id=user.id))

# Read
@api.route('/users/', methods=['GET'])
def read_users():
  users = query_chain(Model = User)
  users_list = []
  for user in users:
    users_list.append(user.to_json())
  return jsonify(users_list)

@api.route('/users/<int:id>', methods=['GET'])
def read_user(id):
  user = query_chain(Model=User, PK_key=id).first_or_404()
  return jsonify([user.to_json()])

# Update
@api.route('/users/<int:id>', methods=["PUT", "PATCH"])
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
  return redirect(url_for('api.read_user', id=user.id), code=code)

# Delete
@api.route('/users/<int:id>', methods=["DELETE"])
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

  # return redirect(url_for('api.read_users'))
  return jsonify({'message': "user deleted"})
