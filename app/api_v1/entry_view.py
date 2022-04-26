from . import api
from flask import jsonify, url_for



@api.route('/')
def index():
  return jsonify(
    {
            "message": "server is running.",
            "status": 200,
            "features": [
                {
                  "endpoint": f'{url_for("api.read_courses", _external=True)}',
                  "description": "endpoint for all courses",
                  "methods": ["GET"]
                },
                {
                  "endpoint": {
                      "url": "/course/{id}",
                      "params": [
                        { "id": "Id of course when deleting, updating or getting a course" }
                      ],
                      "GET-example": f'{url_for("api.read_course", id=123, _external=True)}'
                },
                "description": "endpoint to update, create, and delete a course",
                "methods": ["GET", "POST", "PUT", "PATCH", "DELETE"]
                },
                {
                "endpoint": f'{url_for("api.read_challenges", _external=True)}',
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
                    ], 'GET-example': f'{url_for("api.read_challenge", id=123, _external=True)}',
                },
                "description": "endpoint to update, create, and delete a challenge",
                "methods": ["GET", "POST", "PUT", "PATCH", "DELETE"]
                },
                {
                "endpoint": f'{url_for("api.read_users", _external=True)}',
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
                    ],
                    "GET-example": f'{url_for("api.read_user", id=123, _external=True)}',
                },
                "description": "endpoint to update, create, and delete a user",
                "methods": ["GET", "POST", "PUT", "PATCH", "DELETE"]
                }
            ],
            "WARNING": "SERVER RUNNING USING DEV DB, PROD DB NEEDED! After updating config file, update ENV config setting at init"
        }
  ), 200