from . import auth
from app.models import User
from flask import jsonify, request
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required
from app.api_v1.route_controls import abort_request
from app.email import send_email
from app import db
from datetime import timedelta

@auth.route('/signin/', methods=['POST'])
def signin():
  user = User.find_by_username(request.json.get('username', None))

  if user is None:
    abort_request(message="User does not exists", code=404)
  
  # if not user.verified:
  #   return jsonify({"message": "Account not verified, please check your email and verify your account", "code": 401}), 401
  
  try: 
    if User.verify_hash(request.json.get('password', None), user.password):
      access_token = create_access_token(identity=request.json['username'], expires_delta=timedelta(hours=1))
      return jsonify({'message': f'logged in as {request.json["username"]}', 'access_token': access_token})
    else:
      return jsonify({'message': 'incorrect username or password', 'code': 401}), 401
  except:
    return jsonify({'message': 'invalid input', "code": 422}), 422


@auth.route('/confirm/email/<username>')
# @jwt_required()
def resend_auth_email(username):
  user = db.session.query(User).filter_by(username=username).first()
  if user is None:
    return jsonify({"message": "user does not exists", "code": 404}), 422

  if user.verified:
    return jsonify({"message": "user has already been verified.", 'code': 422}), 422

  try:
    send_email(
      user.email, 
      'Confirm Account', 
      'email/confirm', 
      user=user, 
      token=user.generate_verification_token(user.username)
    )
  except:
    abort_request(message="unable to send email", code=500)
  return jsonify({"message": 'Email has been sent', "code": 200}), 200

@auth.route('/confirm/<token>')
def confirm(token):
  if User.confirm_verification_token(token):
    return jsonify({'message': "Account has been comfirmed"}), 200
  return jsonify({'message': 'unable to confirm account'}), 422

