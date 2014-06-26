from os import getcwd, listdir
from datamapper.app import db
from datamapper.app.models import Data
"""
File format: _, date, value, state
"""

def get_file_list(directory = getcwd()):
    return listdir(directory)

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

def add_to_db(data):
    for dp in data:
        try:
            new_dp = Data(**dp)
            db.session.add(new_dp)
            db.session.commit()
        except Exception as err:
            print(err.message)
            db.session.rollback()