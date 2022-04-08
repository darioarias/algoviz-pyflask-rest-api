from app import app
from flask import jsonify, request


# Create
@app.route('/challenge/', methods=["POST"])
def create_challenges():
  return jsonify({"message": "Post challenges end-point", "status": 200})


# Read
@app.route('/challenges/', methods=["GET"])
def read_challenges():
  return jsonify({"message": "Get all challenges end-point", "status": 200})

@app.route('/challenge/<id>', methods=["GET"])
def read_challenge(id):
  return jsonify({"message": "Get challenges by id end-point", "status": 200})


# Update
@app.route('/challenge/<id>',  methods=["PUT", "PATCH"])
def update_challenge(id):
  if request.method == "PUT":
    return jsonify({"message": "Update via PUT challenge by id end-point", "status": 200})
  
  if request.method == "PATCH":
    return jsonify({"message": "Update via PATCH challenge by id end-point", "status": 200})


# Delete
@app.route('/challenges/<id>', methods=["DELETE"])
def delete_challenges(id):
  return jsonify({"message": "DELETE challenge by id end-point", "status": 200})
