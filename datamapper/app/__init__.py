from os import environ
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__)
db = SQLAlchemy(app)
# app.config.from_object('config')

app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL', 'postgresql://ian:heatmapper@localhost/heatmapper')
app.config['CSRF_ENABLED'] = True
app.config['SECRET_KEY'] = '\xd0\x9bV\x06w 6\x82z\\W\xa2l\xd6L\x99\xbek^ \xcb\xfb\xcc2'

import views, models