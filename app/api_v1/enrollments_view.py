from app import db
from app.models import Enrollment
from flask import jsonify, redirect, request, url_for
from . import api_v1
from .route_controls import abort_request, query_chain
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required

# Create
@api_v1.route('/enrollments/', methods=['POST'])
@jwt_required()
def create_enrollment():
  print(request.json)
  username = request.json.get('username', None);
  course_title = request.json.get('title', None);

  try:
    # db.session.add(enrollment)
    if(Enrollment.enroll_user(username, course_title)):
      db.session.commit()
    else:
      return jsonify({"message": "enrollment already exits or user and/or title were not found", "code": 400})
  except IntegrityError as error:
    abort_request(message='Unable to create enrollment', code=500, details=error.orig.diag.message_detail if error.orig and error.orig.diag else "No user or course found")
  finally:
    db.session.rollback()
  return jsonify({"message": "user has been enrolled", "code": 201})

# Read
@api_v1.route('/enrollments/', methods=['GET'])
def read_enrollments():
  enrollments = query_chain(Model = Enrollment).order_by()
  enrollments_list = []
  for enrollment in enrollments:
    enrollments_list.append(enrollment.to_json())
  return jsonify(enrollments_list)

@api_v1.route('/enrollments/<int:id>', methods=['GET'])
def read_enrollment(id):
  enrollment = query_chain(Model = Enrollment, PK_key=id).first_or_404()
  return jsonify([enrollment.to_json()])

# Update
@api_v1.route('/enrollments/<int:id>', methods=["PUT", "PATCH"])
@jwt_required()
def update_enrollment(id):
  enrollment = query_chain(Model=Enrollment, PK_key=id).first()
  if request.method == "PUT":
    if enrollment is None:
      enrollment = Enrollment(
        course_id = request.json.get('course_id', None),
        user_id = request.json.get('user_id', None)
      )
      db.session.add(enrollment)
    else:
      enrollment.course_id = request.json.get('course_id', None)
      enrollment.user_id = request.json.get('user_id', None)
      enrollment.completed_on = request.json.get('completed_on', None)

  if request.method == "PATCH":
    if enrollment is None:
      abort_request(message='Enrollment does not exists', code=400)
    
    enrollment.course_id = request.json.get('course_id', enrollment.course_id)
    enrollment.user_id = request.json.get('user_id', enrollment.user_id)
    enrollment.completed_on = request.json.get('completed_on', enrollment.completed_on)
  
  try:
    db.session.commit()
  except IntegrityError as error:
    abort_request(message='Unable to update enrollment', code=500, details=error.orig.diag.message_detail)
  finally:
    db.session.rollback()
  
  return redirect(url_for('api_v1.read_enrollment', id=enrollment.id))

# Delete
@api_v1.route('/enrollments/<int:id>', methods=["DELETE"])
@jwt_required()
def delete_enrollment(id):
  enrollment = query_chain(Model=Enrollment, PK_key=id).first();
  if enrollment is None:
    abort_request(message="Enrollment does not exists", code=404)
  
  try:
    db.session.delete(enrollment)
    db.session.commit();
  except IntegrityError as error:
    abort_request(message="Unable to delete enrollment", code=500, details=error.orig.diag.message_detail)
  finally:
    db.session.rollback();
  
  return redirect(url_for('.read_enrollments'))




