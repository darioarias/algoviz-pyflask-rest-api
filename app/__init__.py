from flask import Flask

app = Flask(__name__)

# if app.config["ENV"] == "production":
#     app.config.from_object("config.ProductionConfig")
# else:
#     app.config.from_object("config.DevelopmentConfig")
app.config.from_object("config.ProductionConfig")

from app import entry_view
from app import course_view
from app import challenge_view
from app import user_view

print(f'ENV is set to: {app.config["ENV"]}')
