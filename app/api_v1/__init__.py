from flask import Blueprint
from flask_cors import CORS

api = Blueprint('api', __name__)
CORS(api)
# from . import challenge_view, course_view, user_view, middlewares
# from . import course_view, middlewares
from . import attempts_view, challenges_view, courses_view, user_view, error_handlers, enrolled_view, entry_view
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