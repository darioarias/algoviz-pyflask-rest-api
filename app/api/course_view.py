
from . import api
from flask import jsonify, request, json
import os

# Create
@api.route('/course/', methods=['POST'])
def create_course(id):
    return jsonify({"message": "Post course end-point", "status": 200})


# Read
@api.route('/courses/', methods=['GET'])
def read_courses():
    return jsonify({"message": "all courses end-point", "status": 200})

@api.route('/course/<id>', methods=['GET'])
def read_course(id):
    return jsonify({"message": "Get course by id end-point", "status": 200})

# Update
@api.route('/course/<id>', methods=["PUT", "PATCH"])
def update_course(id):
  if request.method == "PUT":
    return jsonify({"message": "Update via PUT course by id end-point", "status": 200})
  
  if request.method == "PATCH":
    return jsonify({"message": "Update via PATCH course by id end-point", "status": 200})

# Delete
@api.route('/course/<id>', methods=["DELETE"])
def delete_course(id):
    return jsonify({"message": "DELETE course by id end-point", "status": 200})
