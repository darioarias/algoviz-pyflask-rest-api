from flask import Blueprint
from flask_cors import CORS

api_v1 = Blueprint('api_v1', __name__)
CORS(api_v1)

from . import attempts_view, challenges_view, courses_view, enrollments_view, error_handlers, entry_view, users_view
# from . import users_view
# from app import db
# from .models import User

# @main.route('/test')
# def test():
#     courses = db.session.query(Course)
#     # for course in challenges.collections: #artist.album_collection
#         # print(course)
#     for course in courses:
#         print(f'{course.title} - has challenge:')
#         for challenges in course.challenges_collection:
#             print(f'\t{challenges.title}')
#         print('\n')
#     # print(course.challenges_collection)
#     # print(db.metadata.tables)

#     return jsonify({'message':'testing endpoint', 'code': 200})


# def user_query_ch(Count: int = None, Id: int = None):
#   query = db.session.query(User) if Id is None else db.session.query(User).filter(User.id == Id)

#   if(Count is not None):
#     query = query.limit(count)
  
#   if (Id is not None):
#     query = query
  
#   return query
