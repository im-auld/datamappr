from random import random, randint
from flask import render_template, request, redirect, url_for
from flask import jsonify
from datamapper.app import app
from datamapper.app.models import State

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/mock-ajax')
def mock_ajax():
    states = State.query.all()
    coords = [{
                'lat': state.latitude, 
                'lng' : state.longitude, 
                'count' : randint(10000, 100000)} 
                for state in states]
    # mock = [{
    #         'lat' : random() * 60,
    #         'lng' : random() * -180,
    #         'count' : randint(25000, 45000)} 
    #         for _ in range(100)]
    return jsonify(data=coords)