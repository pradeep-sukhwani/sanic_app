# Sanic App

First sanic app to show the imdb movie listing

## Installation

```bash
pip install -r requirements.txt
```

## Setup Local Server
Create ```settings.py``` file in the project root directory and add the following:

```python
HOST = 'localhost'
PORT = '8000'
DEBUG = True
DB_URL = 'sqlite:///imdb.db?charset=utf8'
LOGIN_PASSWORD='<set your desired password to login>' 
```
## Run server:
```bash
python app.py
```

## Load Initial Data
```bash
python load_data.py
```

## Login Email:
```text
Admin:
admin.test@gmail.com
admin.test2@testmail.com

Non Admin:
test.user@testmail.com

Password: Password is the <LOGIN_PASSWORD> mentioned in settings.py
```
