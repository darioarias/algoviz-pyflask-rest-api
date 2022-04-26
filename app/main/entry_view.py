from crypt import methods
from flask import jsonify, json, url_for
import os
from . import main

# Landing
@main.route("/", methods=['GET'])
def index():
    return jsonify(
        {
            "message": "server is running.",
            "status": 200,
            "features": [
                {
                "endpoint": "/courses",
                "description": "endpoint for all courses",
                "methods": ["GET"]
                },
                {
                "endpoint": {
                    "url": "/course/{id}",
                    "params": [
                    { "id": "Id of course when deleting, updating or getting a course" }
                    ]
                },
                "description": "endpoint to update, create, and delete a course",
                "methods": ["GET", "POST", "PUT", "PATCH", "DELETE"]
                },
                {
                "endpoint": "/challenges",
                "description": "endpoint for all challenges",
                "methods": ["GET"]
                },
                {
                "endpoint": {
                    "url": "/challenge/{id}",
                    "params": [
                    {
                        "id": "Id of challenge when deleting, updating or getting a challenge"
                    }
                    ]
                },
                "description": "endpoint to update, create, and delete a challenge",
                "methods": ["GET", "POST", "PUT", "PATCH", "DELETE"]
                },
                {
                "endpoint": "/users",
                "description": "endpoint for all users",
                "methods": ["GET"]
                },
                {
                "endpoint": {
                    "url": "/challenge/{id}",
                    "params": [
                    {
                        "id": "Id of user when deleting, updating or getting a user"
                    }
                    ]
                },
                "description": "endpoint to update, create, and delete a user",
                "methods": ["GET", "POST", "PUT", "PATCH", "DELETE"]
                }
            ],
            "WARNING": "SERVER RUNNING USING DEV DB, PROD DB NEEDED! After updating config file, update ENV config setting at init"
        }
    )
    # filename = os.path.join(app.static_folder, 'json', 'about.json')
    # with open(filename) as about_json:
    #     data = json.load(about_json)
    # return data, 200



# not found error handler
@main.errorhandler(404)
def content_not_found(e):
    print(e)
    return jsonify({"message": "content not found, go to '/' for a full description of endpoints", "code": 404})