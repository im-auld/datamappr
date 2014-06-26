from glob import glob
from os import getcwd, listdir
from datamapper.app import db
from datamapper.app.models import Data
"""
File format: _, date, value, state
"""

def get_file_list(directory = getcwd()):
    return glob('*.csv')

def get_states():
    with open('states.txt')as st:
        keys = ('name', 'short_name', 'latitude', 'longitude')
        states = [dict(zip(keys, state.strip().split(','))) for state in st]
    return states

def get_data_sets():
    data_sets = []
    for ds in get_file_list():
        data_set = ''.join(file.split('.')[0].replace('_',' '))
        data_sets.append(data_set)
    return data_sets

def parse(file, testing=True):
    data_set = ''.join(file.split('.')[0].replace('_',' '))
    keys = ('date', 'raw_data', 'state')
    with open(file) as f:
        data = [dict(zip(keys,line.strip().split(',')[1:])) for line in f]
        for dp in data:
            dp['data_set'] = data_set
    if testing:
        return data[1::int(len(data)*.01)]
    return data

def add_states_to_db(states):
    try:
        for state in states:
            db.session.add(State(**state))
        db.session.commit()
    except Exception as err:
        print(err.message)
        db.session.rollback()
        raise

def add_data_sets_to_db(data_sets):
    try:
        for ds in data_sets:
            db.session.add(State(ds))
        db.session.commit()
    except Exception as err:
        print(err.message)
        db.session.rollback()

def add_data_to_db(data):
    try:
        for dp in data:
            db.session.add(Data(**dp))
        db.session.commit()
    except Exception as err:
        print(err.message)
        db.session.rollback()

if __name__ == '__main__':
    files = get_file_list()
    states = get_states()
    add_states_to_db(states)
    data_sets = get_data_sets()
    add_data_sets_to_db(data_sets)
    for file in files:
        add_data_to_db(parse(file, testing=False))