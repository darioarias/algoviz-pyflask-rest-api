from . import api_v1
from flask import g, jsonify
# from app import dbms


# @api.before_app_request
# def before_request():
#   pass
  # try:
  #   g.db_connection = dbms.get_db_connection()
  # except:
  #   return jsonify({'message': 'internal error', 'code': 500}), 500

# @api.after_app_request
# @api.teardown_appcontext
# def after_request(response):
#   if hasattr(g, 'db_connection'):
#     g.db_connection.close()
#   return response