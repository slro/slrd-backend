"""."""
from flask import Flask
import logging

slrd = Flask(__name__)
from slrd.views import views


logging.getLogger(__name__).addHandler(logging.NullHandler())
