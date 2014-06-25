from os import environ

SQLALCHEMY_DATABASE_URI = environ.get(
    'DATABASE_URL', 'postgresql://localhost/heatmapper'
)