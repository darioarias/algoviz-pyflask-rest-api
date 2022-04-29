from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine
from flask import url_for
import os

Base = automap_base()
engine = create_engine(os.environ.get('SQLALCHEMY_DATABASE_URI')) if os.environ.get('SQLALCHEMY_DATABASE_URI') else None 
if engine is None:
  raise Exception("Unable to reflect Database, please provide proper Database URI")

class User(Base):
  __tablename__ = 'users'

  def to_json(self):
    user_json = {
      "id": self.id,
      "username": self.username,
      "email": self.email,
      "password": self.password,
      'first_name': self.first_name,
      'last_name': self.last_name,
      'joined_date': self.joined_date,
      'last_seen': self.last_seen,
      'url': url_for('api.read_user', id=self.id, _external=True)
    }

    return user_json

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