
from . import api
from flask import jsonify, request, json, g
from app.dbms import Queries as query
import os

# Create
@api.route('/course/', methods=['POST'])
def create_course(id):
    return jsonify({"message": "Post course end-point", "status": 200})


# Read
@api.route('/courses/', methods=['GET'])
def read_courses():
    cur = g.db_connection.cursor()
    cur.execute(query.get_all_courses())
    courses = cur.fetchall()
    cur.close()
    return jsonify(courses)
    return jsonify({"message": "all courses end-point", "status": 200})

@api.route('/course/<int:id>', methods=['GET'])
def read_course(id):
    cur = g.db_connection.cursor()
    cur.execute(query.get_course_by_id(id))
    course = cur.fetchall()
    cur.close()
    return jsonify(course), 200
    return jsonify({"message": "Get course by id end-point", "status": 200})


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
