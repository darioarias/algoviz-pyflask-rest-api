from app import db
from .models import Attempt
from flask import jsonify, request, url_for
from . import api

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
@api.route('/attempt/', methods=['POST'])
def create_attempt():
    return jsonify({"message": "Post user end-point", "status": 200})

# Read
@api.route('/attempts/', methods=['GET'])
def read_attempts():
  attempts = query_chain(Model = Attempt)

  attempts_list = []
  for attempt in attempts:
    attempts_list.append(
      {
        'id': attempt.id, 
        'answer': attempt.attempt_answer, 
        'score': attempt.attemp_score, 
        'submittion_date': attempt.attempted_on, 
        'submitted_by': url_for('api.read_user', id=attempt.user_id, _external=True),#attempt.user_id, 
        'challenge_id': attempt.challenge_id, 
        }
      )
  return jsonify(attempts_list)


@api.route('/attempt/<id>', methods=['GET'])
def read_attempt(id):
  attempt = query_chain(Model = Attempt).first_or_404()
  return jsonify([
    {
      'id': attempt.id, 
      'answer': attempt.attempt_answer, 
      'score': attempt.attemp_score, 
      'submittion_date': attempt.attempted_on, 
      'submitted_by': url_for('api.read_user', id=attempt.user_id, _external=True),#attempt.user_id, 
      'challenge_id': attempt.challenge_id, 
    }
  ])

# Update
@api.route('/attempt/<id>', methods=["PUT", "PATCH"])
def update_attempt(id):
  if request.method == "PUT":
    return jsonify({"message": "Update via PUT user by id end-point", "status": 200})
  
  if request.method == "PATCH":
    return jsonify({"message": "Update via PATCH user by id end-point", "status": 200})

# Delete
@api.route('/attempt/<id>', methods=["DELETE"])
def delete_attempt(id):
    return jsonify({"message": "DELETE user by id end-point", "status": 200})




