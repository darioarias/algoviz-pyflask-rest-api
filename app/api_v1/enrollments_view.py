from app import db
from app.models import Enrollment
from flask import jsonify, redirect, request, url_for
from . import api
from .route_controls import abort_request
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
@api.route('/enrollments/', methods=['POST'])
def create_enrollment():
  enrollment = Enrollment(
    course_id = request.json.get('course_id', None),
    user_id = request.json.get('user_id', None),
  )
  try:
    db.session.add(enrollment)
    db.session.commit()
  except IntegrityError as error:
    abort_request(message='Unable to create enrollment', code=500, details=error.orig.diag.message_detail)
  finally:
    db.session.rollback()
  return redirect(url_for('api.read_enrollment', id=enrollment.id))

# Read
@api.route('/enrollments/', methods=['GET'])
def read_enrollments():
  enrollments = query_chain(Model = Enrollment)
  enrollments_list = []
  for enrollment in enrollments:
    enrollments_list.append(enrollment.to_json())
  return jsonify(enrollments_list)


@api.route('/enrollments/<int:id>', methods=['GET'])
def read_enrollment(id):
  enrollment = query_chain(Model = Enrollment, PK_key=id).first_or_404()
  return jsonify([enrollment.to_json()])

# Update
@api.route('/enrollments/<int:id>', methods=["PUT", "PATCH"])
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
  
  return redirect(url_for('api.read_enrollment', id=enrollment.id))

# Delete
@api.route('/enrollments/<int:id>', methods=["DELETE"])
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




