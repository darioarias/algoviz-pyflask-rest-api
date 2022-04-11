from . import api
from flask import g, jsonify
from app import dbms


@api.before_app_request
def before_request():
  try:
    g.db_connection = dbms.get_db_connection()
  except:
    return jsonify({'message': 'internal error', 'code': 500}), 500

@api.after_app_request
def after_request(response):
  g.db_connection.close()
  return response