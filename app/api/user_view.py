
from . import api
from flask import jsonify, request, json
import os

# Create
@api.route('/user/', methods=['POST'])
def create_user(id):
    return jsonify({"message": "Post user end-point", "status": 200})

# Read
@api.route('/users/', methods=['GET'])
def read_users():
    return jsonify({"message": "all courses end-point", "status": 200})

@api.route('/user/<id>', methods=['GET'])
def read_user(id):
    return jsonify({"message": "Get user by id end-point", "status": 200})

# Update
@api.route('/user/<id>', methods=["PUT", "PATCH"])
def update_user(id):
  if request.method == "PUT":
    return jsonify({"message": "Update via PUT user by id end-point", "status": 200})
  
  if request.method == "PATCH":
    return jsonify({"message": "Update via PATCH user by id end-point", "status": 200})

# Delete
@api.route('/user/<id>', methods=["DELETE"])
def delete_user(id):
    return jsonify({"message": "DELETE user by id end-point", "status": 200})
