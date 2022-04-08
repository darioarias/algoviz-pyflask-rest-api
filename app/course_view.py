
from app import app
from flask import jsonify, request, json
import os

# Create
@app.route('/course/', methods=['POST'])
def create_course(id):
    return jsonify({"message": "Post course end-point", "status": 200})


# Read
@app.route('/courses/', methods=['GET'])
def read_courses():
    return jsonify({"message": "all courses end-point", "status": 200})

@app.route('/course/<id>', methods=['GET'])
def read_course(id):
    return jsonify({"message": "Get course by id end-point", "status": 200})

# Update
@app.route('/course/<id>', methods=["PUT", "PATCH"])
def update_course(id):
  if request.method == "PUT":
    return jsonify({"message": "Update via PUT course by id end-point", "status": 200})
  
  if request.method == "PATCH":
    return jsonify({"message": "Update via PATCH course by id end-point", "status": 200})

# Delete
@app.route('/course/<id>', methods=["DELETE"])
def delete_course(id):
    return jsonify({"message": "DELETE course by id end-point", "status": 200})
