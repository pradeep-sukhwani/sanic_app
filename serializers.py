from marshmallow import Schema, fields


class UserSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    email = fields.String()
    is_admin = fields.Boolean()


class GenreSchema(Schema):
    genre_id = fields.Integer()
    genre_name = fields.String()


class MovieSchema(Schema):
    movie_id = fields.Integer()
    movie_name = fields.String()
    score = fields.Float()
    popularity = fields.Float()
    director = fields.String()
    genre = fields.Nested(GenreSchema(), many=True)
