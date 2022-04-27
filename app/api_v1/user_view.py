from . import api
from flask import jsonify, request, json, g, url_for
# from app.dbms import Queries as query
from .models import User
from app import db

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
@api.route('/user/', methods=['POST'])
def create_user():
    return jsonify({"message": "Post user end-point", "status": 200})

# Read
@api.route('/users/', methods=['GET'])
def read_users():
  # users = db.session.query(User)
  users = query_chain(Model = User)

  users_list = []
  for user in users:
    users_list.append(
      {
        'id': user.id, 
        'username': user.user_name, 
        'email': user.email, 
        'first_name': user.first_name, 
        'last_name':user.last_name, 
        'joined_date':user.joined_date, 
        'last_seen': user.last_visited
        }
      )
  return jsonify(users_list)


@api.route('/user/<id>', methods=['GET'])
def read_user(id):
  user = query_chain(Model=User, PK_key=id).first_or_404()
  for attempt in user.attempts_collection:
    print(url_for('api.read_challenge', id=attempt.challenge_id, _external=True))

  return jsonify(
    [{
      'id': user.id, 
      'username': user.user_name, 
      'email': user.email, 
      'first_name': user.first_name, 
      'last_name':user.last_name, 
      'joined_date':user.joined_date, 
      'last_seen': user.last_visited
      }]
    )

# Update
@api.route('/user/<id>', methods=["PUT", "PATCH"])
def update_user(id):
  if request.method == "PUT":
    return jsonify({"message": "Update via PUT user by id end-point", "status": 200})
  
  if request.method == "PATCH":
    return jsonify({"message": "Update via PATCH user by id end-point", "status": 200})

# Delete
@api.route('/user/<id>', methods=["DELETE"])
def delete_user(id):
    return jsonify({"message": "DELETE user by id end-point", "status": 200})
