import json
import unittest

import requests


class TestOpenAPI(unittest.TestCase):
    def setUp(self):
        # Initialize any necessary variables or configurations
        pass

    def test_get_todos(self):
        # Make a GET request to the /todos/{username} endpoint
        url = 'http://localhost:5003/todos/{username}'
        username = 'test_user'
        response = requests.get(url.format(username=username))

        # Assert the response status code is 200
        self.assertEqual(response.status_code, 200)

        # Assert the response body is a valid JSON with the expected structure
        response_json = response.json()
        self.assertIsInstance(response_json, dict)
        self.assertIn('todos', response_json)
        self.assertIsInstance(response_json['todos'], list)

    def test_add_todo(self):
        # Make a POST request to the /todos/{username} endpoint
        url = 'http://localhost:5003/todos/{username}'
        username = 'test_user'
        todo = 'Test todo'
        payload = {'todo': todo}
        response = requests.post(url.format(username=username), json=payload)

        # Assert the response status code is 200
        self.assertEqual(response.status_code, 200)

        # Assert the response body is a valid JSON with the expected structure
        response_json = response.json()
        self.assertIsInstance(response_json, dict)
        self.assertIn('success', response_json)
        self.assertTrue(response_json['success'])

    def test_delete_todo(self):
        # Make a DELETE request to the /todos/{username} endpoint
        url = 'http://localhost:5003/todos/{username}'
        username = 'test_user'
        todo_idx = 0
        payload = {'todo_idx': todo_idx}
        response = requests.delete(url.format(username=username), json=payload)

        # Assert the response status code is 200
        self.assertEqual(response.status_code, 200)

        # Assert the response body is a valid JSON with the expected structure
        response_json = response.json()
        self.assertIsInstance(response_json, dict)
        self.assertIn('success', response_json)
        self.assertTrue(response_json['success'])

if __name__ == '__main__':
    unittest.main()
