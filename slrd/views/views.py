from slrd import slrd
from flask import render_template


@slrd.route('/')
def index():
    return render_template('index.html')
