from models import User, Movie, Genre, Link
from serializers import UserSchema, MovieSchema, GenreSchema

from utils import check_password, remove_blank_space


def setup_routes(app, jinja, auth, response, data_base_session):
    @app.route("/")
    async def home_page(request):
        user = {}
        session = request.ctx.session.get('session')
        if session:
            user_session = session.get('_auth')
            user_schema = UserSchema()
            user_obj = data_base_session.query(User).filter_by(id=user_session.get('uid')).first()
            user_serializer = user_schema.dump(user_obj)
            user.update(user_serializer)
        return jinja.render(template="movie_list.html", request=request, **{'user': user})

    @app.route('/login', methods=['POST'])
    async def login(request):
        user = data_base_session.query(User).filter_by(email=request.form.get('email')).first()
        if user:
            if check_password(request.form.get('password'), user.password):
                session_data = {'session': {}}
                auth.login_user(session_data, user)
                request.ctx.session.update(session_data)
                return response.json({
                    'success': True, **session_data
                })
            else:
                return response.json({
                    'error': True,
                    'message': "Password does not match",
                }, status=401)
        return response.json({
            'error': True,
            'message': "User not found",
        }, status=404)

    @app.route('/logout', methods=['POST'])
    async def logout(request):
        auth.logout_user(request.ctx.session)
        return response.json({
            'success': True,
            'message': 'Logged out successfully'
        })

    @app.route('/movies', methods=['GET', 'POST', 'PATCH', 'DELETE'])
    async def movies_list(request):
        json_response, status = {}, 200
        movie_schema = MovieSchema()
        if request.method == 'GET':
            # Get all the movie instances
            link_query = data_base_session.query(Movie).filter(Link.movie_id == Movie.movie_id).all()
            movie_serializer = movie_schema.dump(link_query, many=True)
            json_response.update({
                'success': True,
                'message': movie_serializer,
            })
        elif request.method == 'POST':
            # Create new movie instance
            movie_object = data_base_session.query(Movie).filter_by(movie_name=request.form.get('movie_name')).first()
            if movie_object:
                json_response.update({
                    'message': request.form.get('movie_name') + " movie already exist in our database."
                })
                status = 401
            else:
                genre = ",".join(request.form.pop('genre')).split(",")
                new_movie_instance = Movie(movie_name=remove_blank_space(request.form.get('movie_name')),
                                           popularity=request.form.get('popularity'),
                                           score=request.form.get('score'),
                                           director=remove_blank_space(request.form.get('director')))
                for genre_name in genre:
                    genre_instance = data_base_session.query(Genre).filter_by(
                        genre_name=remove_blank_space(genre_name)).first()
                    if not genre_instance:
                        genre_instance = Genre(genre_name=remove_blank_space(genre_name))
                        data_base_session.add(genre_instance)
                    new_movie_instance.genre.append(genre_instance)
                    data_base_session.add(new_movie_instance)
                    data_base_session.commit()
                movie_serializer = movie_schema.dump(new_movie_instance)
                json_response.update({
                    'success': True,
                    'movie_obj': movie_serializer,
                    'message': movie_serializer.get('movie_name') + " Movie was successfully added"
                })
                status = 201
        elif request.method == 'PATCH':
            # Update movie instance
            genre = ",".join(request.form.pop('genre')).split(",")
            movie_obj = data_base_session.query(Movie).filter_by(movie_id=request.form.get('movie_id')).first()
            genre_obj_list = []
            for genre_name in genre:
                genre_obj = data_base_session.query(Genre).filter_by(genre_name=remove_blank_space(genre_name)).first()
                if not genre_obj:
                    genre_obj = Genre(genre_name=remove_blank_space(genre_name))
                    data_base_session.add(genre_obj)
                    data_base_session.commit()
                genre_obj_list.append(genre_obj)
            movie_obj.genre[:] = genre_obj_list
            movie_obj.director = request.form.get('director')
            movie_obj.popularity = request.form.get('popularity')
            movie_obj.score = request.form.get('score')
            movie_obj.movie_name = request.form.get('movie_name')
            data_base_session.add(movie_obj)
            data_base_session.commit()
            movie_serializer = movie_schema.dump(movie_obj)
            json_response.update({
                'success': True,
                'movie_obj': movie_serializer,
                'message': f'Successfully update Movie {request.form.get("name")}.'
            })
        elif request.method == 'DELETE':
            # Delete movie instance
            movie_obj = data_base_session.query(Movie).filter_by(movie_id=request.form.get('movie_id')).first()
            data_base_session.delete(movie_obj)
            data_base_session.commit()
            json_response.update({
                'success': True,
                'message': f'Successfully deleted Movie {request.form.get("name")}.'
            })
        return response.json(json_response, status=status)
