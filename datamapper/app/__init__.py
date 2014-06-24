from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__)
db = SQLAlchemy(app)
app.config.from_object('config')

import views, models