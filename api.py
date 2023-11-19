import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
from datetime import date
import json

from database.models import db_drop_and_create_all, setup_db, Movie, Actor
from auth.auth import AuthError, requires_auth

def create_app(test=False):
    app = Flask(__name__)
    app.config.from_object('config_db')

    if not test:
        setup_db(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        return response

    # ROUTES
    @app.route('/')
    def index():
        return jsonify({
            'success': True,
            'message': 'Welcome to the homepage!'
        }), 200

    # Endpoints GET
    @app.route('/actors', methods=['GET'])
    def get_actors():
        actors = Actor.query.all()
        actor_list = [actor.format() for actor in actors]
        return jsonify({
            'success': True,
            'actors': actor_list
        }), 200

    @app.route('/movies', methods=['GET'])
    def get_movies():
        movies = Movie.query.all()
        movie_list = [movie.format() for movie in movies]
        return jsonify({
            'success': True,
            'movies': movie_list
        }), 200

    # Endpoints POST
    @app.route('/actors', methods=['POST'])
    @requires_auth(permission='post:actors')
    def post_actor(payload):
        body = request.get_json()
        # Check invalid data
        if 'name' not in body or 'age' not in body or 'gender' not in body:
            abort(400, description="Invalid data. Required fields: name, age, gender")
        name = body.get('name', None)
        age = body.get('age', None)
        gender = body.get('gender', None)
        actor = Actor(name=name, age=age, gender=gender)
        actor.insert()
        return jsonify({
            'success': True,
            'actors': [actor.format()]
        }), 200

    @app.route('/movies', methods=['POST'])
    @requires_auth(permission='post:movies')
    def post_movie(payload):
        body = request.get_json()
        # Check invalid data
        if 'title' not in body or 'release_date' not in body:
            abort(400, description="Invalid data. Required fields: title and release_date")
        title = body.get('title', None)
        try:
            release_date = date.fromisoformat(body.get('release_date', None))
        except:
            abort(400, description="Invalid date format. Use ISO format (YYYY-MM-DD)")

        movie = Movie(title=title, release_date=release_date)
        movie.insert()
        return jsonify({
            'success': True,
            'movies': [movie.format()]
        }), 200

    # Endpoint DELETE
    @app.route('/actors/<int:id>', methods=['DELETE'])
    @requires_auth(permission='delete:actors')
    def delete_actor(payload, id):
        actor = Actor.query.filter(Actor.id == id).one_or_none()

        if not actor:
            abort(404, description=f"Actor with id {id} not found")
        actor.delete()

        return jsonify({
            'success': True,
            'message': 'Actor deleted successfully'
        }), 200
    
    @app.route('/movies/<int:id>', methods=['DELETE'])
    @requires_auth(permission='delete:movies')
    def delete_movie(payload, id):
        movie = Movie.query.filter(Movie.id == id).one_or_none()
        
        if not movie:
            abort(404, description=f"Movie with id {id} not found")
        movie.delete()

        return jsonify({
            'success': True,
            'message': 'Movie deleted successfully'
        }), 200
    
    # Endpoint PATCH
    @app.route('/movies/<int:id>', methods=['PATCH'])
    @requires_auth(permission='patch:movies')
    def patch_movie(payload, id):
        movie = Movie.query.filter(Movie.id == id).one_or_none()
        if not movie:
            abort(404, description=f"Movie with id {id} not found")

        body = request.get_json()
        if 'title' not in body or 'release_date' not in body:
            abort(400, description="Invalid data. Required fields: title and release_date")
        title = body.get('title', None)
        try:
            release_date = date.fromisoformat(body.get('release_date', None))
        except:
            abort(400, description="Invalid date format. Use ISO format (YYYY-MM-DD)")

        movie.title = title
        movie.release_date = release_date
        movie.update()

        return jsonify({
            'success': True,
            'movies': [movie.format()]
        }), 200
    
    @app.route('/actors/<int:id>', methods=['PATCH'])
    @requires_auth(permission='patch:actors')
    def patch_actor(payload, id):
        actors = Actor.query.filter(Actor.id == id).one_or_none()
        if not actors:
            abort(404, description=f"Actors with id {id} not found")

        body = request.get_json()
        if 'name' not in body or 'age' not in body or 'gender' not in body:
            abort(400, description="Invalid data. Required fields: name, age, gender")

        actors.name = body.get('name', None)
        actors.age = body.get('age', None)
        actors.gender = body.get('gender', None)
        actors.update()

        return jsonify({
            'success': True,
            'actors': [actors.format()]
        }), 200

    # Error Handling --------------------------------------------------------------

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
        'success': False,
        'error': 404,
        'message': error.description
        }), 404

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': error.description
        }), 400

    @app.errorhandler(AuthError)
    def handle_auth_error(e):
        return jsonify({
            "success": False,
            "error": e.status_code,
            "message": e.error['description']
        }), e.status_code

    return app

app = create_app()
with app.app_context():
    db_drop_and_create_all()

if __name__ == '__main__':
    app.run(debug=True)