import bcrypt
from sqlalchemy import Column, Integer, ForeignKey, String, BOOLEAN, TEXT, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(length=100), nullable=False)
    email = Column(String(length=100), nullable=False, index=True)
    is_admin = Column(BOOLEAN, default=False)
    password = Column(TEXT(convert_unicode=True))

    def __repr__(self):
        return f"<User(id={self.id}, name={self.name}, email={self.email}, is_admin={self.is_admin})>"


class Genre(Base):
    __tablename__ = 'genre'
    genre_id = Column(Integer, primary_key=True)
    genre_name = Column(String(length=50), nullable=False)
    movie = relationship('Movie', secondary='link')

    def __repr__(self):
        return f"<Genre(genre_id={self.genre_id}, genre_name={self.genre_name})>"


class Movie(Base):
    __tablename__ = 'movie'
    movie_id = Column(Integer, primary_key=True)
    movie_name = Column(String(length=100), nullable=False, index=True)
    score = Column(Float(asdecimal=True, precision=1))
    popularity = Column(Float(asdecimal=True, precision=1))
    director = Column(String(length=100))
    genre = relationship(Genre, secondary='link')

    def __repr__(self):
        return f"<Movie(movie_id={self.movie_id}, movie_name={self.movie_name}, score={self.score}, " \
               f"popularity={self.popularity})>"


class Link(Base):
    __tablename__ = 'link'
    link_id = Column(Integer, primary_key=True)
    genre_id = Column(Integer, ForeignKey('genre.genre_id'))
    movie_id = Column(Integer, ForeignKey('movie.movie_id'))

    def __repr__(self):
        return f"<Link(genre_id={self.genre_id}, movie_id={self.movie_id})>"
