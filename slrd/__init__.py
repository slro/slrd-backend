from flask import Flask
from slrd.strings import comlogstr

slrd = Flask(__name__)
from slrd.views import views
