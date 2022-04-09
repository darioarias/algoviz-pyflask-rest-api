from flask import Blueprint, blueprints

main = Blueprint('main', __name__)

from . import entry_view