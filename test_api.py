import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
import logging

from database.models import db_drop_and_create_all, setup_db, Movie, Actor
from config_db import DB_USER, DB_PASSWORD, DB_HOST
from api import create_app

casting_assistan_auth_header = {
    "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InRvTEd4dzVEUHplVVNTb0h1Wmt3TSJ9.eyJpc3MiOiJodHRwczovL3F1eWV0Y3YxLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NTVhNTI0NjVhYWZlOGU4NzQyODc3NGUiLCJhdWQiOiJodHRwOi8vbG9jYWxob3N0OjUwMDAiLCJpYXQiOjE3MDA0MTg2OTMsImV4cCI6MTcwMDUwNTA5MywiYXpwIjoicDQ4TEwwWWl4Y0tERktHT3lQWEdvWThGTzByalVqM1YiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.XXNgOO8wWrlgepw1rdKzaeh5lAJFIHFV-Jg7LDZMUDDhPjqaYJLWTNm29k5PUDcZrn_OMli0DAyTQUi6JggQ23STX0ROH39fVfUR4kmGbIzAbZSANpeMyaMw5VQgk04U86zu3GRO_RTtW7gAY0jvo1AsWh9VfdIQ6xmotSs3vkZ6nbcu0JRwpN7Kg-tUGsjM4qIsE1q-9Wnybqw66G6ZbXX_45KyDpdHpPzCIXejR7tw9k4mGYHWa6S4VIsCEGueMNblvoFWY8AzQaQXn-DS_opJ-F-FT-GUob94Bh9ZKSyBqNdwDDT8jiEOZiqDSVYsIvGFC-rCiFFaNZcNbl6H5w"
}

casting_director_auth_header = {
    "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InRvTEd4dzVEUHplVVNTb0h1Wmt3TSJ9.eyJpc3MiOiJodHRwczovL3F1eWV0Y3YxLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NTVhNTU0YTg3Y2IzMDAzYzg2ZWFiZDgiLCJhdWQiOiJodHRwOi8vbG9jYWxob3N0OjUwMDAiLCJpYXQiOjE3MDA0MTg5OTYsImV4cCI6MTcwMDUwNTM5NiwiYXpwIjoicDQ4TEwwWWl4Y0tERktHT3lQWEdvWThGTzByalVqM1YiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIl19.H05d4isF33-aR1sn-S-C0CSN_XCHmFR_Z-sW4KX2pmdeoPN_QkA2RLLUX970l5dadVKGtGh4WBKSfEIeF9vamnSvy7ez4uWSzQWPpogALTgrUkBCEmytGOGtZW2BU0n-OP_NwLJhI31I_VLTBILI0glkYuPaNIMttjJZb8GC_OlVS6F0t_OpnmwESunJbhUOMknLlwYhIXALwqVfuDN3obciETmP6imIw0K2PfpqQpLo-pjnmPRYM5r0XPkXtJVtTBNDCikvguMV7FVxQMwD0vyxKwjxKCM5X1HYqDnE78UihIP2sXib6L_5BhRNt0LNlENxuf-Tyf_ey_8ja3b1lA"
}

executive_producer_auth_header = {
    "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InRvTEd4dzVEUHplVVNTb0h1Wmt3TSJ9.eyJpc3MiOiJodHRwczovL3F1eWV0Y3YxLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NTVhNTYyNTg3Y2IzMDAzYzg2ZWFjNTUiLCJhdWQiOiJodHRwOi8vbG9jYWxob3N0OjUwMDAiLCJpYXQiOjE3MDA0MTkxODIsImV4cCI6MTcwMDUwNTU4MiwiYXpwIjoicDQ4TEwwWWl4Y0tERktHT3lQWEdvWThGTzByalVqM1YiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.BpP34UzzeWVb8xPyk6u2JfMK-gO_1oaCD8Ijrk7m1ucXBZW6MODj_gyDPhUt9mI08bnyYpnKgeiyJWUo-N7MQ835KMa-cYJH2nUOILR4DQCP83ggnTXqtRSXYWb6W0kc3Tt8HuuaIMCE5QcDH0KtYH7zvo5zgBt6h_Bp-TkxAerNZDqgodM1WKbYkkhqOFrtGgJVYnrInRCnA2t_DFnMHIso__VTZoyG0276Zkg6OOd7AyEsb4FZkG46kWOKKJW2FldBMvnKqScKnDKfz2baBUqsFJcnA513rhroKIb-yBYajE0DPahvynSHlwyxdPx6EYQRlTF6KqI0DsqMc4keKg"
}

logging.basicConfig(level=logging.DEBUG, format='\n%(asctime)s - %(name)s - %(levelname)s - %(message)s')
LOG = logging.getLogger(name='test_api.py')

class CastingAgencyTestCase(unittest.TestCase):
    '''
    This class represents the Casting Agency api test case
    '''
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(test=True)
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        self.database_name = "casting_test"
        self.database_path = 'postgresql://{}:{}@{}/{}'.format(
            DB_USER,
            DB_PASSWORD,
            DB_HOST,
            self.database_name
        )
        setup_db(app=self.app, database_path=self.database_path)
        with self.app.app_context():
            db_drop_and_create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_root(self):
        response = self.client.get('/')
        data = json.loads(response.data)
        LOG.info(data)
        self.assertEqual(response.status_code, 200)
    
    # Test case for Casting Assistan
    def test_get_actors_casting_assistan(self):
        response = self.client.get('/actors', headers=casting_assistan_auth_header)
        data = json.loads(response.data)
        LOG.info(data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
    
    def test_get_movies_casting_assistan(self):
        response = self.client.get('/movies', headers=casting_assistan_auth_header)
        data = json.loads(response.data)
        LOG.info(data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
    
    def test_post_actors_casting_assistan(self):
        actors_json = {
            'name': 'Quyet',
            'age': 24,
            'gender': 'male'
        }
        response = self.client.post('/actors', headers=casting_assistan_auth_header, json=actors_json)
        LOG.info(response.data)
        self.assertEqual(response.status_code, 403)
    
    def test_post_movies_casting_assistan(self):
        movies_json = {
            'title': 'Godzilla Minus One',
            'release_date': '2009-01-01'
        }
        response = self.client.post('/movies', headers=casting_assistan_auth_header, json=movies_json)
        LOG.info(response.data)
        self.assertEqual(response.status_code, 403)
    
    def test_patch_actors_casting_assistan(self):
        actors_json = {
            'name': 'Quyet',
            'age': 24,
            'gender': 'male'
        }
        response = self.client.patch('/actors/1', headers=casting_assistan_auth_header, json=actors_json)
        LOG.info(response.data)
        self.assertEqual(response.status_code, 403)
    
    def test_patch_movies_casting_assistan(self):
        movies_json = {
            'title': 'Godzilla Minus One',
            'release_date': '2009-01-01'
        }
        response = self.client.patch('/movies/1', headers=casting_assistan_auth_header, json=movies_json)
        LOG.info(response.data)
        self.assertEqual(response.status_code, 403)
    
    def test_delete_actors_casting_assistan(self):
        response = self.client.delete('/actors/1', headers=casting_assistan_auth_header)
        LOG.info(response.data)
        self.assertEqual(response.status_code, 403)
    
    def test_delete_movies_casting_assistan(self):
        response = self.client.delete('/movies/1', headers=casting_assistan_auth_header)
        LOG.info(response.data)
        self.assertEqual(response.status_code, 403)
    
    # Test case for Casting Director
    def test_get_actors_casting_director(self):
        response = self.client.get('/actors', headers=casting_director_auth_header)
        data = json.loads(response.data)
        LOG.info(data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
    
    def test_get_movies_casting_director(self):
        response = self.client.get('/movies', headers=casting_director_auth_header)
        data = json.loads(response.data)
        LOG.info(data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
    
    def test_post_actors_casting_director(self):
        actors_json = {
            'name': 'Quyet',
            'age': 24,
            'gender': 'male'
        }
        response = self.client.post('/actors', headers=casting_director_auth_header, json=actors_json)
        data = json.loads(response.data)
        LOG.info(data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
    
    def test_post_movies_casting_director(self):
        movies_json = {
            'title': 'Godzilla Minus One',
            'release_date': '2009-01-01'
        }
        response = self.client.post('/movies', headers=casting_director_auth_header, json=movies_json)
        LOG.info(response.data)
        self.assertEqual(response.status_code, 403)
    
    def test_patch_actors_casting_director(self):
        actors_json = {
            'name': 'Quyet',
            'age': 24,
            'gender': 'male'
        }
        response = self.client.patch('/actors/1', headers=casting_director_auth_header, json=actors_json)
        data = json.loads(response.data)
        LOG.info(data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
    
    def test_patch_movies_casting_director(self):
        movies_json = {
            'title': 'Godzilla Minus One',
            'release_date': '2009-01-01'
        }
        response = self.client.patch('/movies/1', headers=casting_director_auth_header, json=movies_json)
        data = json.loads(response.data)
        LOG.info(data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
    
    def test_delete_actors_casting_director(self):
        response = self.client.delete('/actors/1', headers=casting_director_auth_header)
        data = json.loads(response.data)
        LOG.info(data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
    
    def test_delete_movies_casting_director(self):
        response = self.client.delete('/movies/1', headers=casting_director_auth_header)
        LOG.info(response.data)
        self.assertEqual(response.status_code, 403)
    
    def test_patch_actors_casting_director_not_found_id(self):
        actors_json = {
            'name': 'Quyet',
            'age': 24,
            'gender': 'male'
        }
        response = self.client.patch('/actors/255', headers=casting_director_auth_header, json=actors_json)
        LOG.info(response.data)
        self.assertEqual(response.status_code, 404)
    
    def test_patch_actors_casting_director_invalid_data(self):
        actors_json = {
            'name': 'Quyet',
            'gender': 'male'
        }
        response = self.client.patch('/actors/1', headers=casting_director_auth_header, json=actors_json)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)

    def test_delete_actors_casting_director_not_found_id(self):
        response = self.client.delete('/actors/255', headers=casting_director_auth_header)
        LOG.info(response.data)
        self.assertEqual(response.status_code, 404)
    
    # Test case for Executive Producer
    def test_get_actors_executive_producer(self):
        response = self.client.get('/actors', headers=executive_producer_auth_header)
        data = json.loads(response.data)
        LOG.info(data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
    
    def test_get_movies_executive_producer(self):
        response = self.client.get('/movies', headers=executive_producer_auth_header)
        data = json.loads(response.data)
        LOG.info(data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
    
    def test_post_actors_executive_producer(self):
        actors_json = {
            'name': 'Quyet',
            'age': 24,
            'gender': 'male'
        }
        response = self.client.post('/actors', headers=executive_producer_auth_header, json=actors_json)
        data = json.loads(response.data)
        LOG.info(data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
    
    def test_post_movies_executive_producer(self):
        movies_json = {
            'title': 'Godzilla Minus One',
            'release_date': '2009-01-01'
        }
        response = self.client.post('/movies', headers=executive_producer_auth_header, json=movies_json)
        data = json.loads(response.data)
        LOG.info(data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
    
    def test_patch_actors_executive_producer(self):
        actors_json = {
            'name': 'Quyet',
            'age': 24,
            'gender': 'male'
        }
        response = self.client.patch('/actors/1', headers=executive_producer_auth_header, json=actors_json)
        data = json.loads(response.data)
        LOG.info(data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
    
    def test_patch_movies_executive_producer(self):
        movies_json = {
            'title': 'Godzilla Minus One',
            'release_date': '2009-01-01'
        }
        response = self.client.patch('/movies/1', headers=executive_producer_auth_header, json=movies_json)
        data = json.loads(response.data)
        LOG.info(data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
    
    def test_delete_actors_executive_producer(self):
        response = self.client.delete('/actors/1', headers=executive_producer_auth_header)
        data = json.loads(response.data)
        LOG.info(data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
    
    def test_delete_movies_executive_producer(self):
        response = self.client.delete('/movies/1', headers=executive_producer_auth_header)
        data = json.loads(response.data)
        LOG.info(data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
    
    def test_patch_actors_executive_producer_not_found_id(self):
        actors_json = {
            'name': 'Quyet',
            'age': 24,
            'gender': 'male'
        }
        response = self.client.patch('/actors/255', headers=executive_producer_auth_header, json=actors_json)
        LOG.info(response.data)
        self.assertEqual(response.status_code, 404)
    
    def test_patch_actors_executive_producer_invalid_data(self):
        actors_json = {
            'name': 'Quyet',
            'gender': 'male'
        }
        response = self.client.patch('/actors/1', headers=executive_producer_auth_header, json=actors_json)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)

    def test_delete_actors_executive_producer_not_found_id(self):
        response = self.client.delete('/actors/255', headers=executive_producer_auth_header)
        LOG.info(response.data)
        self.assertEqual(response.status_code, 404)
    
    # Test case not include headers
    def test_get_actors_not_include_header(self):
        response = self.client.get('/actors')
        LOG.info(response.data)
        self.assertEqual(response.status_code, 401)
    
    def test_get_movies_not_include_header(self):
        response = self.client.get('/movies')
        LOG.info(response.data)
        self.assertEqual(response.status_code, 401)

    def test_post_movies_not_include_header(self):
        movies_json = {
            'title': 'Godzilla Minus One',
            'release_date': '2009-01-01'
        }
        response = self.client.post('/movies', json=movies_json)
        LOG.info(response.data)
        self.assertEqual(response.status_code, 401)

if __name__ == "__main__":
    unittest.main()