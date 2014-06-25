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

@app.route('/get-data-set', methods=['POST', 'GET'])
def get_data_set():
    print(request.args)
    data_set = request.args.get('data_set', False)
    date_start = request.args.get('date_start', False)
    date_end = request.args.get('date_end', True)
    return jsonify(
        data_set=data_set,
        date_start=date_start,
        date_end=date_end
        )