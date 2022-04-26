from flask import Flask
from config import config
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine
# from flask_cors import CORS

import os

import click
from flask.cli import with_appcontext

db = SQLAlchemy()

Base = automap_base()
engine = create_engine(os.environ.get('SQLALCHEMY_DATABASE_URI')) if os.environ.get('SQLALCHEMY_DATABASE_URI') else None 
if(not engine):
  raise Exception("Unable to reflect Database, please provide proper Database URI")
Base.prepare(engine, reflect=True)

def create_app(config_name):
  app = Flask(__name__)
  # cors = CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
  app.config.from_object(config[config_name])
  config[config_name].init_app(app)
  db.init_app(app)

  # app.cli.add_command(reflect_db)
  # with app.app_context():
    # db.Model.metadata.reflect(bind=db.engine)
  # with app.app_context():
  # print()
  from .main import main as main_blueprint
  app.register_blueprint(main_blueprint)

  from .api_v1 import api as api_v1_blueprint
  app.register_blueprint(api_v1_blueprint, url_prefix='/api/v1/')

  print('running on http://127.0.0.1:5000/api/v1')
  return app


# def get_db_handle(db):
#   from sqlalchemy.ext.automap import automap_base
#   from sqlalchemy import create_engine
#   Base = automap_base(db.Model)
#   engine = create_engine('postgresql://xymzimekksmhco:46887cbb0d16af42586a19224f5b3a37a1ce8f60b6bf15c182f36963a1c5c854@ec2-23-20-224-166.compute-1.amazonaws.com:5432/d3n66vadq0jsq8')
#   Base.prepare(engine, reflect=True)

#   return Base

# print(f'ENV is set to: {app.config["ENV"]}')
@click.command('reflect-db')
@with_appcontext
def reflect_db():
  pass
  # print("TESTING")
  # import psycopg2
  # from sqlalchemy.ext.automap import automap_base
  # from sqlalchemy import create_engine
  # print('test... Dario_te')

  # Base = automap_base(db.Model)
  # engine = create_engine('postgresql://xymzimekksmhco:46887cbb0d16af42586a19224f5b3a37a1ce8f60b6bf15c182f36963a1c5c854@ec2-23-20-224-166.compute-1.amazonaws.com:5432/d3n66vadq0jsq8')
  # Base.prepare(engine, reflect=True)
  # print(db.metadata.tables['challenges'])


  # db.Model = automap_base(db.Model)
  # from app import models
  # db.Model.prepare(engine, reflect=True)
  # print(db.metadata.tables)

  # # for record in db.session.query(Base.classes.challenges).all():
  #   print(record)
