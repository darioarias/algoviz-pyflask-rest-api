
from app import app
from flask import jsonify, request, json
import os

# Create
@app.route('/user/', methods=['POST'])
def create_user(id):
    return jsonify({"message": "Post user end-point", "status": 200})

# Read
@app.route('/users/', methods=['GET'])
def read_users():
    return jsonify({"message": "all courses end-point", "status": 200})

@app.route('/user/<id>', methods=['GET'])
def read_user(id):
    return jsonify({"message": "Get user by id end-point", "status": 200})

# Update
@app.route('/user/<id>', methods=["PUT", "PATCH"])
def update_user(id):
  if request.method == "PUT":
    return jsonify({"message": "Update via PUT user by id end-point", "status": 200})
  
  if request.method == "PATCH":
    return jsonify({"message": "Update via PATCH user by id end-point", "status": 200})

# Delete
@app.route('/user/<id>', methods=["DELETE"])
def delete_user(id):
    return jsonify({"message": "DELETE user by id end-point", "status": 200})
