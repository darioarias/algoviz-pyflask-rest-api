from app import app
from flask import jsonify, request, json
import os


# Landing
@app.route("/", methods=['GET'])
def index():
    filename = os.path.join(app.static_folder, 'json', 'about.json')
    with open(filename) as about_json:
        data = json.load(about_json)
    return data

# not found error handler
@app.errorhandler(404)
def content_not_found(e):
    print(e)
    return jsonify({"message": "content not found, go to '/' for a full description of endpoints", "code": 404})