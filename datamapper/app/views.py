from random import random, randint
from flask import render_template, request, redirect, url_for
from flask import jsonify
from datamapper.app import app
from datamapper.app.models import State
from datamapper.app.forms import DataSetForm

@app.route('/')
@app.route('/index')
def index():
    form = DataSetForm()
    form.data_set.choices = [(1,'Unemployment'), (2,'GDP'), (3,'Housing Starts')]
    return render_template('index.html', form=form)

@app.route('/mock-ajax')
def mock_ajax():
    states = State.query.all()
    coords = [{
        'lat': state.latitude,
        'lng': state.longitude,
        'count': random()}
        for state in states]
    max_val = max([coord['count'] for coord in coords])
    print(max_val)
    return jsonify(data=coords, max_val=max_val)