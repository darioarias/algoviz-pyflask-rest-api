
from . import api
from flask import jsonify, request, json, g
from .models import Course, User
from app import db
# from app.dbms import Queries as query
# from app.dbms import DBMS as query
from sqlalchemy import select
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


# Create
@api.route('/course/', methods=['POST'])
def create_course(id):
    return jsonify({"message": "Post course end-point", "status": 200})


# Read
@api.route('/courses/', methods=['GET'])
def read_courses():
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
  return jsonify(course_list)

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
  if request.method == "PUT":
    return jsonify({"message": "Update via PUT course by id end-point", "status": 200})
  
  if request.method == "PATCH":
    return jsonify({"message": "Update via PATCH course by id end-point", "status": 200})


# Delete
@api.route('/course/<int:id>', methods=["DELETE"])
def delete_course(id):
    return jsonify({"message": "DELETE course by id end-point", "status": 200})
