from flask import Flask
from config import config
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine
import os

db = SQLAlchemy()
Base = automap_base()
engine = create_engine(os.environ.get('SQLALCHEMY_DATABASE_URI')) if os.environ.get('SQLALCHEMY_DATABASE_URI') else None 
if(not engine):
  raise Exception("Unable to reflect Database, please provide proper Database URI")
Base.prepare(engine, reflect=True)

def create_app(config_name):
  app = Flask(__name__)
  app.config.from_object(config[config_name])
  config[config_name].init_app(app)
  db.init_app(app)

  from .main import main as main_blueprint
  app.register_blueprint(main_blueprint)

  from .api_v1 import api as api_v1_blueprint
  app.register_blueprint(api_v1_blueprint, url_prefix='/api/v1/')

  print('running on http://127.0.0.1:5000/api/v1')
  return app