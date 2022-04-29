from . import api
from flask import jsonify, request, json, abort, Response, redirect, url_for
from .route_controls import abort_request
from app.models import Course
from app import db
from sqlalchemy.exc import IntegrityError, DatabaseError

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

# def abort_request(message: str = None, code: int = 500, details = None):
#   response = Response(
#     json.dumps({
#       'message': message,
#       'code': code,
#       'error': details if details is not None else "no details provided"
#     }), status=code, content_type='application/json'
#   )
#   abort(response)

def model_course(resource: object):
  entry = {
    'title': resource.get('title' or None),
    'description': resource.get('description' or None),
    'url': resource.get('url' or None), 
  }

  if not entry['title'] or not entry['description']:
    abort_request(message="course title and description must be provided", code=400)
  
  if(entry['url']):
    newCourse = Course(title=entry['title'], course_url=entry['url'], course_description=entry['description']);
  else:
    newCourse = Course(title=entry['title'], course_description=entry['description']);

  return newCourse


# Create
@api.route('/courses/', methods=['POST'])
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
  return redirect(url_for('api.read_course', id=course.id))

# Read
@api.route('/courses/', methods=['GET'])
def read_courses():
  try: 
    courses = query_chain(Model=Course)
    course_list = []
    for course in courses:
      course_list.append(course.to_json())
  except:
    abort_request(message="Internal Server Error")
  return jsonify(course_list) if len(course_list) >= 1 else jsonify([{'message': "no courses found"}])

@api.route('/courses/<int:id>', methods=['GET'])
def read_course(id):
  course = query_chain(Model=Course, PK_key=id).first_or_404()
  course_list = [course.to_json()]
  return jsonify(course_list), 200


# Update
@api.route('/courses/<int:id>', methods=["PUT", "PATCH"])
def update_course(id):
  course = query_chain(Model=Course, PK_key=id).first()
  code = 200
  if request.method == "PUT": #update, create if it does not exist
    if course is None:
      code = 201
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
  return redirect(url_for('api.read_course', id=course.id), code=code)

# Delete
@api.route('/courses/<int:id>', methods=["DELETE"])
def delete_course(id):
  course = query_chain(Model=Course, PK_key=id).first();
  if course is None:
    abort_request(message="Course does not exists", code=400)
  
  db.session.delete(course)
  db.session.commit()

  return redirect(url_for('api.read_courses'))
