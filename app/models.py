from itsdangerous import URLSafeTimedSerializer as Serializer
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine, false
from flask import url_for, current_app
from passlib.hash import pbkdf2_sha256 as sha256
from app import db
from datetime import datetime
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
    courses = db.session.query(Course.title, Enrollment.start_date)
    courses = courses.filter(User.id == Enrollment.user_id)
    courses = courses.filter(Enrollment.course_id == Course.id)
    courses = courses.filter(User.id == self.id)

    challenges = db.session.query(Challenge.title, Challenge.url, Challenge.level)
    challenges = challenges.filter(Attempt.user_id == self.id)
    challenges = challenges.filter(Challenge.id == Attempt.challenge_id)

    format_course = lambda record : {'title': record[0], 'start_date': record[1]}
    format_challenge = lambda record : {'title': record[0], 'url': record[1], 'level': record[2]}

    for record in challenges:
      print(record)

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
      'url': url_for('api_v1.read_user', username=self.username, _external=True),  #[record for record in db.session.query(self).join(Enrollment)]
      'courses': [format_course(record) for record in courses],
      'challenges': [format_challenge(record) for record in challenges]
    }

class Course(Base):
  __tablename__ = 'courses'

  def find_by_title(title):
    return db.session.query(Course).filter_by(title=tile).first()

  def to_json(self):
    query = db.session.query(User.username, User.first_name, User.last_name).filter(User.id == Enrollment.user_id)
    query = query.filter(Enrollment.course_id == self.id)

    format_record = lambda record: {'username': record[0], 'Full_Name': f'{record[1]} {record[2]}'}
    return {
      'id': self.id,
      'title': self.title,
      'url': self.url,
      'description': self.description,
      'students': [format_record(record) for record in query]
    }

class Challenge(Base):
  __tablename__ = 'challenges'

  @staticmethod
  def ralated_to_course(course_id):
    challenges = db.session.query(Challenge)
    challenges = challenges.filter(Challenge.course_id == course_id).order_by(Challenge.level.asc())
    # .filter(Challenge.course_id == course_id).order_by(Challenge.level.asc()).all()
    return challenges

  def to_json(self):
    challenge_json = {
      'id': self.id,
      'title': self.title,
      'course_id': self.course_id,
      'url': self.url,
      'level': self.level
    }
    return challenge_json

class Attempt(Base):
  __tablename__ = 'attempts'
  
  @staticmethod
  def update_attempt(username, challenge_id):
    user = User.find_by_username(username);
    challenge = db.session.query(Challenge).filter(Challenge.id==challenge_id)
    if not user or not challenge:
      return False
    
    attempt = db.session.query(Attempt).filter(Attempt.user_id == user.id).filter(Attempt.challenge_id == challenge_id).first();
    if attempt is not None:
      attempt.last_attempt = datetime.utcnow()
      db.session.add(attempt)
      return True

    else:
      db.session.add(Attempt(user_id=user.id, challenge_id=challenge_id))
      return True;

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

  @staticmethod
  def enroll_user(username, title):
    user = db.session.query(User).filter_by(username=username).first();
    course = db.session.query(Course).filter_by(title=title).first();
    print('user_id', user.id, 'course_id', course.id)
    if (user is None or course is None):
      return False;
    
    enrolment = db.session.query(Enrollment).filter(Enrollment.user_id==user.id).filter(Enrollment.course_id==course.id).first();
    if enrolment is not None:
      return False

    db.session.add(Enrollment(course_id=course.id, user_id=user.id))
    return True
  
  def to_json(self):
    return {
      'id': self.id,
      'course_id': self.course_id,
      'user_id': self.user_id,
      'start_date': self.start_date,
      'completed_on': self.completed_on
    }


Base.prepare(engine, reflect=True)