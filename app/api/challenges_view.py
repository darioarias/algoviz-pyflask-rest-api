from flask import jsonify, request
from . import api
from app import db
from .models import Challenge
from flask import url_for

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
@api.route('/challenge/', methods=["POST"])
def create_challenges():
  return jsonify({"message": "Post challenges end-point", "status": 200})


# Read
@api.route('/challenges/', methods=["GET"])
def read_challenges():
  challenges = query_chain(Model=Challenge)
  challenges_list = []
  for challenge in challenges:
    challenges_list.append(
      {
        'id': challenge.id,
        'title': challenge.title,
        'parent_course': url_for('api.read_course', id=challenge.course_id, _external=True), #challenge.course_id
        'parent_id': challenge.course_id,
        'description': challenge.description
      }
    )
  return jsonify(challenges_list)

@api.route('/challenge/<int:id>', methods=["GET"])
def read_challenge(id):
  challenge = query_chain(Model=Challenge, PK_key=id).first_or_404()

  return jsonify([
    {
      'id': challenge.id,
      'title': challenge.title,
      'parent_course': url_for('api.read_course', id=challenge.course_id, _external=True),
      'parent_id': challenge.course_id,
      'description': challenge.description
    }
  ])


# Update
@api.route('/challenge/<id>',  methods=["PUT", "PATCH"])
def update_challenge(id):
  if request.method == "PUT":
    return jsonify({"message": "Update via PUT challenge by id end-point", "status": 200})
  
  if request.method == "PATCH":
    return jsonify({"message": "Update via PATCH challenge by id end-point", "status": 200})


# Delete
@api.route('/challenges/<id>', methods=["DELETE"])
def delete_challenges(id):
  return jsonify({"message": "DELETE challenge by id end-point", "status": 200})
