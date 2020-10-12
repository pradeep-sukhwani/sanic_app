# Sanic App

First sanic app to show the imdb movie listing

## Installation

```bash
pip install -r requirements.txt
```

## Run server
```bash
python app.py
```

## Login Email
```text
Admin
admin.test@gmail.com
admin.test2@testmail.com

Non Admin
test.user@testmail.com

Password: Default login Password: sanic_123. You can change it: LOGIN_PASSWORD mentioned in settings.py
```

## API
```python
url = '/login'
method = 'POST'
payload = {
    'email': 'testmail@gmail.com',
    'password': 'sanic_123',
}
# Create and return session 


url = '/logout'
method = 'POST'
payload = {
# Expects the session created from login api
}
# return success message

url = '/movies'
method = 'GET'
# return an array of movie instances

url = '/movies'
method = 'POST'
payload = {
'movie_name': 'Star Wars',
'popularity': 98.5,
'score': 9.5,
'director': 'test director',
'genre': 'Action, Fantasy, Adventure', # expects comma separted values
}
# return serialized movie instance

url = '/movies'
method = 'PATCH'
payload = {
'movie_id': 1,
'movie_name': 'Star Wars',
'popularity': 98.5,
'score': 9.5,
'director': 'test director',
'genre': 'Action, Fantasy, Adventure', # expects comma separted values
}
# return serialized movie instance

url = '/movies'
method = 'DELETE'
payload = {
'movie_id': 1,
}
# return success message
```
