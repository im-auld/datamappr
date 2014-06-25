from os import environ
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__)
db = SQLAlchemy(app)
app.config.from_object('config')
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL', 'postgresql://ian:heatmapper@localhost/heatmapper')

import views, models