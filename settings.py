import os

HOST = '0.0.0.0'
PORT = os.environ.get('PORT', '5000')
DEBUG = True
DB_URL = 'sqlite:///imdb.db?charset=utf8'
LOGIN_PASSWORD = 'sanic_123'
