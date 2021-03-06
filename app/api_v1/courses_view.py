from . import api_v1
from flask import jsonify, request, redirect, url_for
from .route_controls import abort_request, query_chain
from app.models import Course
from app import db
from sqlalchemy.exc import IntegrityError, DatabaseError
from flask_jwt_extended import jwt_required

# Create
@api_v1.route('/courses/', methods=['POST'])
@jwt_required()
def create_course():
  course = Course(
    title=request.json.get('title', None),
    url=request.json.get('url', None),
    description=request.json.get('description', None),
  )
  try:
    db.session.add(course)
    db.session.commit()
  except IntegrityError as error:
    abort_request(
      "Unable to create course",
      code = 400,
      details= error.orig.diag.message_detail
    )
  return redirect(url_for('api_v1.read_course', id=course.id))

# Read
@api_v1.route('/courses/', methods=['GET'])
def read_courses():
  try: 
    courses = query_chain(Model=Course)
    course_list = []
    for course in courses:
      course_list.append(course.to_json())
  except:
    abort_request(message="Internal Server Error")
  return jsonify(course_list) if len(course_list) >= 1 else jsonify([{'message': "no courses found"}])

@api_v1.route('/courses/<int:id>', methods=['GET'])
def read_course(id):
  course = query_chain(Model=Course, PK_key=id).first_or_404()
  course_list = [course.to_json()]
  return jsonify(course_list), 200


# Update
@api_v1.route('/courses/<int:id>', methods=["PUT", "PATCH"])
@jwt_required()
def update_course(id):
  course = query_chain(Model=Course, PK_key=id).first()
  if request.method == "PUT": #update, create if it does not exist
    if course is None:
      course = Course(
        title = request.json.get('title', None),
        url = request.json.get('url', None),
        description = request.json.get('description', None)
      )
      db.session.add(course)

    else:
      course.title = request.json.get('title', None)
      course.url = request.json.get('url', None)
      course.description = request.json.get('description', None)
    # return Response(json.dumps({"message": "PUT is not supported", "status": 404}), status=404, content_type='application/json')
  
  if request.method == "PATCH": #partial
    if course is None:
      abort_request(message='Course does not exist', code = 400)
    course.title = request.json.get('title', course.title)
    course.url = request.json.get('url', course.url)
    course.description = request.json.get('description', course.description)

  try:
    db.session.commit()
  except IntegrityError as error:
    abort_request(message='Unable to update record', details = error.orig.diag.message_detail)
  finally:
    db.session.rollback()
  return redirect(url_for('api_v1.read_course', id=course.id))

# Delete
@api_v1.route('/courses/<int:id>', methods=["DELETE"])
@jwt_required()
def delete_course(id):
  course = query_chain(Model=Course, PK_key=id).first();
  if course is None:
    abort_request(message="Course does not exists", code=400)
  
  db.session.delete(course)
  db.session.commit()

  return jsonify({"message": "Course has been deleted!", "code": 200})
