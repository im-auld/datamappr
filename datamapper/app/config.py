from os import environ

DATABASE = environ.get(
    'DATABASE_URL', 'dbname=heatmapper'
)