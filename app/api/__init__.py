from flask import Blueprint

api = Blueprint('api', __name__)
from . import challenge_view, course_view, user_view