from flask import Response, abort, json

def abort_request(message: str = None, code: int = 500, details = None):
  response = Response(
    json.dumps({
      'message': message,
      'code': code,
      'error': details if details is not None else "no details provided"
    }), status=code, content_type='application/json'
  )
  abort(response)