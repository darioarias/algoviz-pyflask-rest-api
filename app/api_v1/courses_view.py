from . import api
from flask import jsonify, request, json, g, abort, Response, redirect, url_for
from .models import Course
from app import db
from sqlalchemy.exc import IntegrityError, DatabaseError
# from datetime import datetime
# from app.dbms import Queries as query
# from app.dbms import DBMS as query
# from sqlalchemy import select
# from .models import Courses
# from .models import User, Attempt, Challenge, Course, 

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

def abort_request(message: str = None, code: int = 500, details = None):
  response = Response(
    json.dumps({
      'message': message,
      'code': code,
      'error': details if details is not None else "no details provided"
    }), status=code, content_type='application/json'
  )
  abort(response)

def model_course(resource: object):
  entry = {
    'title': resource.get('title' or None),
    'description': resource.get('description' or None),
    'url': resource.get('url' or None), 
  }

  if not entry['title'] or not entry['description']:
    abort_request(message="course title and description must be provided", code=400)
    # abort(Response(json.dumps({"message": "course title and description must be provided", 'code': 400}), status=400, content_type='application/json')) #400, description = {'message': 'course title and description must be provided'}
    #400, jsonify(message = 'course title and description must be provided')
  
  if(entry['url']):
    newCourse = Course(title=entry['title'], course_url=entry['url'], course_description=entry['description']);
  else:
    newCourse = Course(title=entry['title'], course_description=entry['description']);

  return newCourse


# Create
@api.route('/course/', methods=['POST'])
def create_course():
  newEntry = model_course(request.json);
  try:
    db.session.add(newEntry)
    db.session.commit()
  except IntegrityError as error:
    abort_request(
      "One or more unique values you tried to insert arealdy exists in the database",
      code = 400,
      details= error.orig.diag.message_detail
    )
  return redirect(url_for('api.read_course', id=newEntry.id))

# Read
@api.route('/courses/', methods=['GET'])
def read_courses():
  try: 
    courses = query_chain(Model=Course)
    course_list = []
    for course in courses:
      course_list.append(
        {
          'id': course.id,
          'title': course.title,
          'url': course.course_url,
          'description': course.course_description
        }
      )
  except:
    abort_request(message="Internal Server Error")
  return jsonify(course_list) if len(course_list) >= 1 else jsonify([{'message': "no courses found"}])

@api.route('/course/<int:id>', methods=['GET'])
def read_course(id):
  course = query_chain(Model=Course, PK_key=id).first_or_404()
  course_list = [
    {
      'id': course.id,
      'title': course.title,
      'url': course.course_url,
      'description': course.course_description
    }
  ]
  return jsonify(course_list), 200


# Update
@api.route('/course/<int:id>', methods=["PUT", "PATCH"])
def update_course(id):
  if request.method == "PUT": #update, create if it does not exist
    return Response(json.dumps({"message": "PUT is not supported", "status": 404}), status=404, content_type='application/json')
  
  if request.method == "PATCH": #partial
    course = query_chain(Model=Course, PK_key=id).first()

    if course is None:
      abort_request(message='Course does not exist', code = 400)

    if 'title' in request.json:
      course.title = request.json['title'];
    
    if 'url' in request.json:
      course.course_url = request.json['url'];
    
    if 'description' in request.json:
      course.course_description = request.json['description']

    try:
      db.session.commit()
    except IntegrityError as error:
      abort_request(message='Unable to update record', code = 400, details = error.orig.diag.message_detail)
    return redirect(url_for('api.read_course', id=course.id))

# Delete
@api.route('/course/<int:id>', methods=["DELETE"])
def delete_course(id):
  course = query_chain(Model=Course, PK_key=id).first();
  if course is None:
    abort_request(message="Course does not exists", code=400)
  
  db.session.delete(course)
  db.session.commit()

  return redirect(url_for('api.read_courses'))
