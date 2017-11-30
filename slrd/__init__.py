from flask import Flask
from slrd.exceptions import *
from slrd.strings import comlogstr

slrd = Flask(__name__)
from slrd import views
