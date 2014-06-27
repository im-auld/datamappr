from os import environ

SQLALCHEMY_DATABASE_URI = environ.get(
    'DATABASE_URL', 'postgresql://ian:heatmapper@localhost/heatmapper')

CSRF_ENABLED = True
SECRET_KEY = '\xd0\x9bV\x06w 6\x82z\\W\xa2l\xd6L\x99\xbek^ \xcb\xfb\xcc2'