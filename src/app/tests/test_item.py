import unittest
from app import app
from http import HTTPStatus
from db import db

class TestItemList(unittest.TestCase):

    def setUp(self) -> None:
        """Creates a new Database for Testing"""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self) -> None:
        """Cleanup DB"""
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_item_list_get_returns_empty_list(self):
        req_route = '/items'
        response = self.client.get(req_route)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.content_type, 'application/json')
        # Assert that response is empty, no items are in DB.
        self.assertEqual(response.get_json(), [])

    def test_item_list_get_returns_non_empty_list(self):
        req_route = '/items'
        req_json = {'description': 'test', 'name': 'test'}
        # Insert Data with Post request.
        response = self.client.post(req_route, json = req_json)

        # Should return 201
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertEqual(response.content_type, 'application/json')
        # Should return an object which was posted.
        self.assertEqual(response.get_json(), req_json)
       
        response = self.client.get(req_route)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.content_type, 'application/json')
        # Assert that response is not empty, test data is there.
        self.assertEqual(response.get_json(), [req_json])

    def test_item_list_post_inserts_new_data(self):
        req_route = '/items'
        req_json = {'description': 'test', 'name': 'test'}
        # Insert Data with Post request.
        response = self.client.post(req_route, json = req_json)

        # Should return 201
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertEqual(response.content_type, 'application/json')
        # Should return an object which was posted.
        self.assertEqual(response.get_json(), req_json)

    def test_item_list_post_invalid_description(self):
        req_route = '/items'
        req_json = {'description': '', 'name': 'test'}
        # Insert Data with Post request.
        response = self.client.post(req_route, json = req_json)
        print(response.get_json())

        # Should return 400
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response.content_type, 'application/json')
        # Should return description about invalid description.
        self.assertEqual(response.get_json(), {'description': ['Shorter than minimum length 1.']})

    def test_item_list_post_invalid_name(self):
        req_route = '/items'
        req_json = {'description': 'test', 'name': 'test'}
        # Insert Data with Post request.
        response = self.client.post(req_route, json = req_json)
        # Insert same Data for the second time to trigger duplicate name validation error.
        response = self.client.post(req_route, json = req_json)

        # Should return 400
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response.content_type, 'application/json')
        # Should return description about invalid name.
        self.assertEqual(response.get_json(), {'name': ['test already exists, please use a different name']})

class TestItem(unittest.TestCase):

    def setUp(self) -> None:
        """Creates a new Database for Testing"""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self) -> None:
        """Cleanup DB"""
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_get_not_found(self):
        req_route = '/items/1'
        response = self.client.get(req_route)

        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(response.content_type, 'application/json')
        # Assert that response is equal to our message.
        self.assertEqual(response.get_json(), {'message': 'item with id: 1 not found'})

    def test_get_returns_inserted_item(self):
        req_route = '/items/1'
        req_json = {'description': 'test', 'name': 'test'}
        response = self.client.put(req_route, json = req_json)
        response = self.client.get(req_route)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.content_type, 'application/json')
        # Assert that response is equal to our request message.
        self.assertEqual(response.get_json(), req_json)

    def test_put_insert(self):
        req_route = '/items/1'
        req_json = {'description': 'test', 'name': 'test'}
        response = self.client.put(req_route, json = req_json)

        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertEqual(response.content_type, 'application/json')
        # Assert that response is equal to our Json request.
        self.assertEqual(response.get_json(), req_json)

    def test_put_update(self):
        req_route = '/items/1'
        req_json = {'description': 'test', 'name': 'test'}
        response = self.client.put(req_route, json = req_json)
        # Send a PUT request again with same ID, to update it.
        req_json = {'description': 'updated', 'name': 'updated'}
        response = self.client.put(req_route, json = req_json)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.content_type, 'application/json')
        # Assert that response is equal to our Json request.
        self.assertEqual(response.get_json(), {'description': 'updated', 'name': 'updated'})

    def test_delete_not_found(self):
        req_route = '/items/1'
        response = self.client.delete(req_route)

        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(response.content_type, 'application/json')
        # Assert that response is equal to our Json request.
        self.assertEqual(response.get_json(), {'message': 'item with id: 1 not found'})

    def test_delete_successfully_deleted(self):
        req_route = '/items/1'
        req_json = {'description': 'test', 'name': 'test'}
        # Insert test item to be deleted.
        response = self.client.put(req_route, json = req_json)
        response = self.client.delete(req_route)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.content_type, 'application/json')

if __name__ == '__main__':
    unittest.main()