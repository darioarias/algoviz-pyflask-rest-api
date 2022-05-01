from itsdangerous import URLSafeTimedSerializer as Serializer
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine, false
from flask import url_for, current_app
from passlib.hash import pbkdf2_sha256 as sha256
from app import db
import os

Base = automap_base()
engine = create_engine(os.environ.get('SQLALCHEMY_DATABASE_URI')) if os.environ.get('SQLALCHEMY_DATABASE_URI') else None 
if engine is None:
  raise Exception("Unable to reflect Database, please provide proper Database URI")

class User(Base):
  __tablename__ = 'users'
  
  @classmethod
  def find_by_username(self, username):
    query = db.session.query(self)
    return query.filter_by(username = username).first()

  @staticmethod
  def generate_hash(password):
    return sha256.hash(password)

  @staticmethod
  def verify_hash(password, hash):
    if password is None:
      return False
    return sha256.verify(password, hash)
  
  @classmethod
  def generate_verification_token(self, username, expiration=3600):
    serializer = Serializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(username, salt=current_app.config['SECURITY_PASSWORD_SALT'])
    # print("WORKUGN WITH: ", self.username, email)
    # print(self.email)
    # return serializer.dumps(self.username, salt="verify")
  
  @staticmethod
  def confirm_verification_token(token, expiration=3600):
    serializer = Serializer(current_app.config['SECRET_KEY'])

    try:
      username = serializer.loads(token, salt=current_app.config['SECURITY_PASSWORD_SALT'], max_age=expiration)
    except:
      return False
    
    user = db.session.query(User).filter_by(username=username).first()
    
    if user is None:
      return False

    if username != user.username:
      return False

    if user.verified:
      return True
    
    try:
      user.verified = True
      db.session.commit()
      return True
    except:
      return False


  
  def to_json(self):
    return {
      "id": self.id,
      "username": self.username,
      "email": self.email,
      "password": self.password,
      'first_name': self.first_name,
      'last_name': self.last_name,
      'joined_date': self.joined_date,
      'last_seen': self.last_seen,
      'verified': self.verified,
      'url': url_for('api_v1.read_user', id=self.id, _external=True)
    }

class Course(Base):
  __tablename__ = 'courses'

  def to_json(self):
    course_json = {
      'id': self.id,
      'title': self.title,
      'url': self.url,
      'description': self.description
    }
    return course_json

class Challenge(Base):
  __tablename__ = 'challenges'

  def to_json(self):
    challenge_json = {
      'id': self.id,
      'title': self.title,
      'course_id': self.course_id,
      'description': self.description
    }
    return challenge_json

class Attempt(Base):
  __tablename__ = 'attempts'

  def to_json(self):
    return {
      'id': self.id,
      'answer': self.answer,
      'score': self.score,
      'last_attempt': self.last_attempt,
      'user_id': self.user_id,
      'challenge_id': self.challenge_id
    }

class Enrollment(Base):
  __tablename__ = 'enrollments'

  def to_json(self):
    return {
      'id': self.id,
      'course_id': self.course_id,
      'user_id': self.user_id,
      'start_date': self.start_date,
      'completed_on': self.completed_on
    }


Base.prepare(engine, reflect=True)