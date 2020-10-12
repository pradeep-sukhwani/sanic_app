import os
import json

from sanic import Sanic
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

import settings
from models import User, Movie, Genre
from utils import get_hashed_password, remove_blank_space


def load_data():
    app = Sanic(__name__)
    app.static('static', './static')
    app.config.update_config(settings)
    engine = create_engine(app.config.DB_URL, echo=True, connect_args={'check_same_thread': False},
                           poolclass=StaticPool)
    data_base_session = sessionmaker(bind=engine, autoflush=False)
    data_base_session = data_base_session()
    database_objects = []
    user_data = [
        {
            'name': 'Pradeep Sukhwani',
            'email': 'admin.test@gmail.com',
            'is_admin': 1,
            'password': get_hashed_password(app.config.LOGIN_PASSWORD),
        },
        {
            'name': 'Test User',
            'email': 'test.user@testmail.com',
            'is_admin': 0,
            'password': get_hashed_password(app.config.LOGIN_PASSWORD),
        },
        {
            'name': 'Test User 2',
            'email': 'admin.test2@testmail.com',
            'is_admin': 1,
            'password': get_hashed_password(app.config.LOGIN_PASSWORD),
        }
    ]
    for item in user_data:
        user_object = data_base_session.query(User).filter_by(email=item.get('email')).first()
        if not user_object:
            database_objects.append(User(**item))
    data_base_session.bulk_save_objects(database_objects)
    data_base_session.commit()

    with open(os.path.join(os.getcwd(), 'imdb.json t.json')) as file_obj:
        json_data = json.loads(file_obj.read())
    genre_list = [remove_blank_space(genre_name) for item in json_data for genre_name in item.get('genre')]
    for genre_name in genre_list:
        genre_object = data_base_session.query(Genre).filter_by(genre_name=genre_name).first()
        if not genre_object:
            genre_object = Genre(genre_name=genre_name)
            data_base_session.add(genre_object)
            data_base_session.commit()
    for item in json_data:
        movie_name = remove_blank_space(item.get('name'))
        current_data = {
            'popularity': item.get('99popularity'),
            'score': item.get('imdb_score'),
            'movie_name': movie_name,
            'director': remove_blank_space(item.get('director'))
        }
        movie_object = data_base_session.query(Movie).filter_by(movie_name=movie_name).first()
        new_object = False
        if not movie_object:
            movie_object = Movie(**current_data)
            new_object = True

        # Get or Create Genre Object
        genre = item.get('genre')
        if new_object:
            for title in genre:
                genre_name = remove_blank_space(title)
                genre_object = data_base_session.query(Genre).filter_by(genre_name=genre_name).first()
                movie_object.genre.append(genre_object)
        data_base_session.add(movie_object)
        data_base_session.commit()
    data_base_session.close_all()
    return True


if __name__ == '__main__':
    load_data()
