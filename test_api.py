import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
import logging

from database.models import db_drop_and_create_all, setup_db, Movie, Actor
from config_db import DB_USER, DB_PASSWORD, DB_HOST
from api import create_app

casting_assistan_auth_header = {
    "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InRvTEd4dzVEUHplVVNTb0h1Wmt3TSJ9.eyJpc3MiOiJodHRwczovL3F1eWV0Y3YxLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NTU5OTM3ZDM5ZThiYmI2ZGRiYmU3YzYiLCJhdWQiOiJodHRwOi8vbG9jYWxob3N0OjUwMDAiLCJpYXQiOjE3MDAzNjkzMzgsImV4cCI6MTcwMDQ1NTczOCwiYXpwIjoicDQ4TEwwWWl4Y0tERktHT3lQWEdvWThGTzByalVqM1YiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.Fsvhnalk9wGUTrDBYPdMffnDA9nXkXctK5G0Z8wuoEJu3d5H-R-rC5oktazRZExOivl5ETtv0GVpL66iVHzxATDqpYFk0A2oiVQYyLdlMzgSea--HOTRUe1yWabgRfldkfMFw12T0AojOv4vT7J21-nu5ky_DQfo-bTC3xEZ22ociNX_5gedM5a84lKsOgP31QcJZpzSVTFn9a-DNcFhn6sWOLL2_kNfOvBoVbBtHCybKyxhNQaOjDDmjG4SO5HdnvEVLnDXPUwA30CSw9vXlN0XxhBFPb-4y7jwjTG01zIkUDjbiTdP7bL9ADv6oQm2bohTEyT18NO9iDh2Xk_Gjg"
}

casting_director_auth_header = {
    "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InRvTEd4dzVEUHplVVNTb0h1Wmt3TSJ9.eyJpc3MiOiJodHRwczovL3F1eWV0Y3YxLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NTI0ZDA2ODczMzQ0YjcwN2M2MmQ4YmUiLCJhdWQiOiJodHRwOi8vbG9jYWxob3N0OjUwMDAiLCJpYXQiOjE3MDAzNjkxMDMsImV4cCI6MTcwMDQ1NTUwMywiYXpwIjoicDQ4TEwwWWl4Y0tERktHT3lQWEdvWThGTzByalVqM1YiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIl19.WiKdzaDrmAuoF2ab67Lb8ogPcaWx1ZDWewWXgtEnsYBloTVkLsGApf3_gpWNnxCSAtXeSzopfxnD0CxHAlY7o6JPdoJNE9hhkMcCO-fIo9ynG6zHdncZX9Dc_zSHSQXoVMA0iX14nVIgaCoi4Dr5NHn4mTOW1oiafXd4Z6DaBzGlVkabffd0qUyCj7kSwZAkfH_yFt7Yks2PFZBSC5hd5g8ZjprVbQMYl5QjYA-bcNu5TMF5Osd9OW7Dt4J1b2__rkD0NNmK9_bmjqu8Yn2rT60ivDSUCveH4_M1mzLOLmu2RW3Rwqi1OoBPMTBwrnH4OWqji18eeT9Pzomvx0aDWg"
}

executive_producer_auth_header = {
    "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InRvTEd4dzVEUHplVVNTb0h1Wmt3TSJ9.eyJpc3MiOiJodHRwczovL3F1eWV0Y3YxLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NTI3YWYwYjZmZWJmMTQyZjFkZTAxM2EiLCJhdWQiOiJodHRwOi8vbG9jYWxob3N0OjUwMDAiLCJpYXQiOjE3MDAzNjg5OTcsImV4cCI6MTcwMDQ1NTM5NywiYXpwIjoicDQ4TEwwWWl4Y0tERktHT3lQWEdvWThGTzByalVqM1YiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.gNs1YK3BqdB2okTG3iO-ywlQddE8GRbvmgsE8aVdd_3pN382U9sFzXkppFiFLd1vYHNGdA9jp_0_up3d_GSgxPj-yQULKnk70UZST1OAL9e9tVLpqG02N1ehkZWH5Zj6OJCDUaqdmlfHqh7sSowPE_vLBu4LU8DqN8vRgfDSZVM31AWx-1uChCJxiuFnnuHYmKdOWDQ4RGpl6Y_UxnltZ1N70av-oEwd99o43nMWtTkL4fjercQCIB-GytTzoAxY8tXHMzi49svdoRKFWkj8MU7tTJBQ_pp6CCNXWhFocuoo_5VcB5slO3R4iQmtYRAcIAZaFXzgt1QbOTopVbKdgg"
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

if __name__ == "__main__":
    unittest.main()