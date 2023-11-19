import os
from sqlalchemy import Column, String, Integer, Date, ForeignKey
from flask_sqlalchemy import SQLAlchemy
from datetime import date
import json

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''

def setup_db(app, database_path=None):
    app.config.from_object('config_db')
    if database_path is not None:
        app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    with app.app_context():
        db.drop_all()
        db.create_all()
    return db



'''
db_drop_and_create_all()
    drops the database tables and starts fresh
    can be used to initialize a clean database
'''

def db_drop_and_create_all():
    db.drop_all()
    db.create_all()
    movie = Movie(
        title='Harry Potter',
        release_date=date(2002, 1, 1)
    )
    actor = Actor(
        name='Daniel Radcliffe',
        age=34,
        gender='Male',
        movie=movie
    )

    movie.insert()
    actor.insert()

# Models

'''
Movie
    a persistent Movie entity, extends the base SQLAlchemy Model
'''
class Movie(db.Model):
    __tablename__ = 'movies'

    # Autoincrementing, unique primary key
    id = Column(Integer().with_variant(Integer, "postgresql"), primary_key=True)
    # String Title
    title = Column(String(80), index=True)
    release_date = Column(Date)

    # Relationship with actors
    actors = db.relationship("Actor", back_populates="movie")

    '''
    insert()
        inserts a new model into a database
        the model must have a unique name
        the model must have a unique id or null id
    '''
    def insert(self):
        db.session.add(self)
        db.session.commit()

    '''
    delete()
        deletes a new model into a database
        the model must exist in the database
    '''
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    '''
    update()
        updates a new model into a database
        the model must exist in the database
    '''
    def update(self):
        db.session.commit()

    def format(self):
        return {
            'id' : self.id,
            'title' : self.title,
            'release_date' : self.release_date
        }
    
    def __repr__(self):
        return f'<Movie(id={self.id}, title={self.title}, release_date={self.release_date})>'

class Actor(db.Model):
    __tablename__ = 'actors'

    id = db.Column(Integer().with_variant(Integer, "postgresql"), primary_key=True)
    name = db.Column(String)
    age = db.Column(Integer)
    gender = db.Column(String)
    
    # Foreign key relationship with movies
    movie_id = db.Column(Integer, ForeignKey('movies.id'))
    movie = db.relationship("Movie", back_populates="actors")

    '''
    insert()
        inserts a new model into a database
        the model must have a unique name
        the model must have a unique id or null id
    '''
    def insert(self):
        db.session.add(self)
        db.session.commit()

    '''
    delete()
        deletes a new model into a database
        the model must exist in the database
    '''
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    '''
    update()
        updates a new model into a database
        the model must exist in the database
    '''
    def update(self):
        db.session.commit()

    def format(self):
        return {
            'id' : self.id,
            'name' : self.name,
            'age' : self.age,
            'gender' : self.gender
        }

    def __repr__(self):
        return f'<Actor(id={self.id}, name={self.name}, age={self.age}, gender={self.gender})>'