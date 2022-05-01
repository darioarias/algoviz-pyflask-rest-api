from flask import Response, abort, json
from app import db

def abort_request(message: str = None, code: int = 500, details = None):
  response = Response(
    json.dumps({
      'message': message,
      'code': code,
      'error': details if details is not None else "no details provided"
    }), status=code, content_type='application/json'
  )
  abort(response)

def query_chain(Model, PK_key: int = None, Count: int = None):
  if(Model is None):
    raise Exception('Model must be provided')

  query = db.session.query(Model)

  if PK_key is not None:
    query = query.filter(Model.id == PK_key)
  
  if Count is not None:
    query = query.limit(Count)
  
  return query