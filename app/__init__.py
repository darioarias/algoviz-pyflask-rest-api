from flask import Flask
from config import config
app = Flask(__name__)

# if app.config["ENV"] == "production":
#     app.config.from_object("config.ProductionConfig")
# else:
#     app.config.from_object("config.DevelopmentConfig")
# app.config.from_object("config.ProductionConfig")

def create_app(config_name):
  app = Flask(__name__)
  app.config.from_object(config[config_name])
  config[config_name].init_app(app)

  from .main import main as main_blueprint
  app.register_blueprint(main_blueprint, url_prefix='/api/v1')

  from .api import api as api_blueprint
  app.register_blueprint(api_blueprint, url_prefix='/api/v1')

  return app

# from app.main import entry_view
# from app import course_view
# from app import challenge_view
# from app import user_view

print(f'ENV is set to: {app.config["ENV"]}')
