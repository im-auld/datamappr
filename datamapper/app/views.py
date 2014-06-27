from datetime import date, datetime
from random import random, randint
from time import strptime
from flask import render_template, request, redirect, url_for
from flask import jsonify
from datamapper.app import app
from datamapper.app.models import State, Data, DataSet
from datamapper.app.forms import DataSetForm

@app.route('/')
@app.route('/index')
def index():
    form = DataSetForm()
    form.data_set.choices = [(ds.id, ds.name) for ds in DataSet.query.all()]
    form.data_set.choices.insert(0, (0,"Please select a dataset"))
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


def format_date(str_date):
    if not str_date:
        return False
    fmt_date = strptime(str_date, '%m/%d/%Y')
    return date(fmt_date.tm_year, fmt_date.tm_mon, fmt_date.tm_mday)


@app.route('/get-start-date', methods=['POST', 'GET'])
def get_start_date():
    data_set = request.args.get('data_set', False)
    first_date = min([dp.date for dp in Data.query.filter(Data.data_set == data_set)])
    first_date = datetime.strftime(first_date, '%m/%d/%Y')
    return jsonify(first_date=first_date)


@app.route('/get-date-range', methods=['POST', 'GET'])
def get_date_range():
    data_set = request.args.get('data_set', False)
    date_start = format_date(request.args.get('date_start', False))
    date_end = format_date(request.args.get('date_end', False))
    if date_end:
        result = Data.query.filter(Data.data_set == data_set).filter(Data.date.between(date_start, date_end)).all()
    else:
        result = Data.query.filter(Data.data_set == data_set).filter().all()
    date_range = sorted(set([str(d.date) for d in result]))
    return jsonify(
            date_range=date_range
        )


def format_data(data):
    result = [{
            'count' : d.raw_data,
            'state' : d.state_id}
            for d in data]
    states = {s.id:{'lat':s.latitude, 'lng': s.longitude} for s in State.query.all()}
    for res in result:
        res['lat'] = states[res['state']]['lat']
        res['lng'] = states[res['state']]['lng']
        del res['state']
    print(result)
    return result


@app.route('/get-data-set', methods=['POST', 'GET'])
def get_data_set():
    print(request.args)
    data_set = request.args.get('data_set', False)
    data_date = request.args.get('date', False)
    print(data_date)
    data_date = [int(d) for d in data_date.split('-')]
    print(data_date)
    data_date = date(*data_date)
    data = Data.query.filter(Data.data_set == data_set).filter(Data.date == data_date).all()
    result = format_data(data)
    max_val = max([res['count'] for res in result])
    return jsonify(data=result, max_val=max_val)