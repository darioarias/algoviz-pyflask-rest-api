from flask import jsonify, redirect, request
from .route_controls import abort_request
from . import api
from app import db
from app.models import Challenge
from flask import url_for
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
@api.route('/challenges/', methods=["POST"])
def create_challenges():
  challenge = Challenge(
    title = request.json.get('title', None),
    course_id = request.json.get('course_id', None),
    description = request.json.get('description', None)
  )
  try:
    db.session.add(challenge)
    db.session.commit()
  except IntegrityError as error:
    print(error.orig.diag)
    abort_request('Unable to create challenge', code=500, details=error.orig.diag.message_detail)
  finally:
    db.session.rollback()
  return redirect(url_for('api.read_challenge', id=challenge.id), code=201)

# Read
@api.route('/challenges/', methods=["GET"])
def read_challenges():
  challenges = query_chain(Model=Challenge)
  challenges_list = []
  for challenge in challenges:
    challenges_list.append(challenge.to_json())
  return jsonify(challenges_list)

@api.route('/challenges/<int:id>', methods=["GET"])
def read_challenge(id):
  challenge = query_chain(Model=Challenge, PK_key=id).first_or_404()
  return jsonify([challenge.to_json()])

# Update
@api.route('/challenges/<int:id>',  methods=["PUT", "PATCH"])
def update_challenge(id):
  challenge = query_chain(Model=Challenge, PK_key=id).first()
  code = 200
  if request.method == "PUT":
    code = 201
    if challenge is None:
      challenge = Challenge(
        title=request.json.get('title', None),
        course_id=request.json.get('course_id', None),
        description=request.json.get('description', None)
      )
      db.session.add(challenge)
    else:
      challenge.title = request.json.get('title', None)
      challenge.course_id = request.json.get('course_id', None)
      challenge.description = request.json.get('description', None)
  
  if request.method == "PATCH":
    if challenge is None:
      abort_request(message="Challenge does not exists", code=400)
    challenge.title = request.json.get('title', challenge.title)
    challenge.course_id = request.json.get('course_id', challenge.course_id)
    challenge.description = request.json.get('description', challenge.description)

  try:
    db.session.commit()
  except IntegrityError as error:
    abort_request(message="Unable to update Challenges", code=500, details=error.orig.diag.message_detail)
  finally:
    db.session.rollback()
  return redirect(url_for('api.read_challenge', id=challenge.id), code=code)

# Delete
@api.route('/challenges/<int:id>', methods=["DELETE"])
def delete_challenges(id):
  challenge = query_chain(Model=Challenge, PK_key=id).first()
  if challenge is None:
    abort_request(message='Challenge does not exits', code=400)
  try:
    db.session.delete(challenge)
    db.session.commit()
  except IntegrityError as error:
    abort_request(message="Unable to delete challenege", code=500, details=error.orig.diag.message_detail)
    
  return redirect(url_for('api.read_challenges'))
