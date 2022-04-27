from crypt import methods
from flask import jsonify, json, url_for
import os
from . import main

# Landing
@main.route("/", methods=['GET'])
def index():
    return jsonify(
        {
            "message": f'welcome to algoViz API, go to this link for version 1 of the API. Link: {url_for("api.index", _external=True)}',
            "code": 200
        }
    )

# not found error handler
@main.errorhandler(404)
def content_not_found(e):
    print(e)
    return jsonify({"message": "content not found, go to '/' for a full description of endpoints", "code": 404}), 404