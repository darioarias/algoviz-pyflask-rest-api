from app import db
from app.models import Attempt
from flask import jsonify, request, url_for, redirect
from . import api
from sqlalchemy.exc import IntegrityError
from .route_controls import abort_request

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
@api.route('/attempts/', methods=['POST'])
def create_attempt():
  attempt = Attempt(
    answer=request.json.get('answer', None),
    score=request.json.get('score', None),
    user_id=request.json.get('user_id', None),
    challenge_id=request.json.get('challenge_id', None),
  )
  
  try:
    db.session.add(attempt)
    db.session.commit()
  except IntegrityError as error:
    abort_request(message="Unable to create Attempt", code=500, details=error.orig.diag.message_detail)
  finally:
    db.session.rollback()
  return redirect(url_for('.read_attempt', id=attempt.id))

# Read
@api.route('/attempts/', methods=['GET'])
def read_attempts():
  attempts = query_chain(Model = Attempt)
  attempts_list = []
  for attempt in attempts:
    attempts_list.append(attempt.to_json())
  return jsonify(attempts_list)

@api.route('/attempts/<int:id>', methods=['GET'])
def read_attempt(id):
  attempt = query_chain(Model = Attempt, PK_key=id).first_or_404()
  return jsonify([attempt.to_json()])


# Update
@api.route('/attempts/<int:id>', methods=["PUT", "PATCH"])
def update_attempt(id):
  attempt = query_chain(Model=Attempt, PK_key=id).first()
  if request.method == "PUT":
    if attempt is None:
      attempt = Attempt(
        answer=request.json.get('answer', None),
        score=request.json.get('score', None),
        user_id=request.json.get('user_id', None),
        challenge_id=request.json.get('challenge_id', None),
      )
      db.session.add(attempt)
    else:
      attempt.answer = request.json.get('answer', None)
      attempt.score = request.json.get('score', None)
      attempt.user_id = request.json.get('user_id', None)
      attempt.challenge_id = request.json.get('challenge_id', None)
  if request.method == "PATCH":
    if attempt is None:
      abort_request(message="Attempt does not exits", code=400)
    attempt.answer = request.json.get('answer', attempt.answer)
    attempt.score = request.json.get('score', attempt.score)
    attempt.user_id = request.json.get('user_id', attempt.user_id)
    attempt.challenge_id = request.json.get('challenge_id', attempt.challenge_id)

  try:
    db.session.add(attempt)
    db.session.commit()
  except IntegrityError as error:
    abort_request(message="Unable to update attempt", code=500, details=error.orig.diag.message_detail)
  finally:
    db.session.rollback()
  return redirect(url_for('.read_attempt', id=attempt.id))

# Delete
@api.route('/attempts/<int:id>', methods=["DELETE"])
def delete_attempt(id):
  attempt = query_chain(Model=Attempt, PK_key=id).first()
  if attempt is None:
    abort_request(message="Attempt does not exits", code=400)
  
  try:
    db.session.delete(attempt)
    db.session.commit()
  except IntegrityError as error:
    abort_request('Unable to delete attempt', code=500, details=error.orig.diag.message_detail)
  finally:
    db.session.rollback();

  return redirect(url_for('.read_users'))




