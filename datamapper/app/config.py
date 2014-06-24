from os import environ

SQLALCHEMY_DATABASE_URI = environ.get(
    'DATABASE_URL', 'postgresql://ian:heatmapper@localhost/heatmapper'
)