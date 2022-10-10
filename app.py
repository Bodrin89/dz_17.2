
from flask import Flask, request
from flask_restx import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
app.config['RESTX_JSON'] = {'ensure_ascii': False, 'indent': 4}
db = SQLAlchemy(app)


class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    description = db.Column(db.String(255))
    trailer = db.Column(db.String(255))
    year = db.Column(db.Integer)
    rating = db.Column(db.Float)
    genre_id = db.Column(db.Integer, db.ForeignKey("genre.id"))
    genre = db.relationship("Genre")
    director_id = db.Column(db.Integer, db.ForeignKey("director.id"))
    director = db.relationship("Director")


class MovieSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.String()
    description = fields.String()
    trailer = fields.String()
    year = fields.Int()
    rating = fields.Float()
    genre_id = fields.Int()
    director_id = fields.Int()


class Director(db.Model):
    __tablename__ = 'director'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


class Genre(db.Model):
    __tablename__ = 'genre'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


api = Api(app)
movie_ns = api.namespace('movies')


@movie_ns.route('/')
class MovieView(Resource):
    def get(self):
        director_id = request.args.get('director_id')
        genre_id = request.args.get('genre_id')
        if director_id:
            movie_schema = MovieSchema(many=True)
            director_id_movie = db.session.query(Movie).filter(Movie.director_id == director_id).all()
            return movie_schema.dump(director_id_movie), 200
        if genre_id:
            movie_schema = MovieSchema(many=True)
            genre_id_movie = db.session.query(Movie).filter(Movie.genre_id == genre_id).all()
            return movie_schema.dump(genre_id_movie), 200
        movie_schema = MovieSchema(many=True)
        all_movies = db.session.query(Movie).all()
        return movie_schema.dump(all_movies), 200


@movie_ns.route('/<int:id>')
class MovieView(Resource):
    def get(self, id: int):
        movie_schema = MovieSchema()
        id_movie = db.session.query(Movie).get(id)
        return movie_schema.dump(id_movie), 200


if __name__ == '__main__':
    app.run(debug=True)
