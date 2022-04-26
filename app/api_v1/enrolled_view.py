from app import db
from .models import Enroll
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
@api.route('/enrollment/', methods=['POST'])
def create_enrollment():
    return jsonify({"message": "Post user end-point", "status": 200})

# Read
@api.route('/enrollments/', methods=['GET'])
def read_enrollments():
  enrollments = query_chain(Model = Enroll)
  enrollments_list = []
  for enrollment in enrollments:
    enrollments_list.append(
      {
        'id': enrollment.id, 
        'course_id': enrollment.course_id, 
        'user_id': enrollment.user_id, 
        'start_date': enrollment.start_date, 
        'completed_on': enrollment.completed_on,
      }
    )
  return jsonify(enrollments_list)


@api.route('/enrollment/<id>', methods=['GET'])
def read_enrollment(id):
  enrollment = query_chain(Model = Enroll, PK_key=id).first_or_404()
  return jsonify([
    {
      'id': enrollment.id, 
      'course_id': enrollment.course_id, 
      'user_id': enrollment.user_id, 
      'start_date': enrollment.start_date, 
      'completed_on': enrollment.completed_on,
    }
  ])

# Update
@api.route('/enrollment/<id>', methods=["PUT", "PATCH"])
def update_enrollment(id):
  if request.method == "PUT":
    return jsonify({"message": "Update via PUT user by id end-point", "status": 200})
  
  if request.method == "PATCH":
    return jsonify({"message": "Update via PATCH user by id end-point", "status": 200})

# Delete
@api.route('/enrollment/<id>', methods=["DELETE"])
def delete_enrollment(id):
    return jsonify({"message": "DELETE user by id end-point", "status": 200})




