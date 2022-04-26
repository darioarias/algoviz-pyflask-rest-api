from . import api
from flask import jsonify, url_for


@api.errorhandler(404)
def not_found(e):
  return jsonify({'message': f'Resource endpoint not found, make sure that all paremeters are spelled correctly. Try vising landing page: {url_for("main.index", _external=True)}', 'code': 404 }), 404