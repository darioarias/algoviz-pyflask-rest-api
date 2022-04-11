from flask import Flask
from config import config
app = Flask(__name__)

def create_app(config_name):
  app = Flask(__name__)
  app.config.from_object(config[config_name])
  config[config_name].init_app(app)

  from .main import main as main_blueprint
  app.register_blueprint(main_blueprint, url_prefix='/api/v1')

  from .api import api as api_blueprint
  app.register_blueprint(api_blueprint, url_prefix='/api/v1')

  return app


print(f'ENV is set to: {app.config["ENV"]}')
print('running on http://127.0.0.1:5000/api/v1')