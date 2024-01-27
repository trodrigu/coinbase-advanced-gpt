import unittest, FlaskTestCase
from unittest.mock import patch, client

from app import app, client


class TestGetTimeRoute(FlaskTestCase):
    @patch.object(client, 'get_unix_time')
    @patch.object(client, 'get_unix_time')
    def test_get_time(self, mock_get_unix_time):
        # Mock the get_unix_time method to return a predefined server time
        mock_get_unix_time.return_value = 1634567890

        # Use the Flask test client to make a GET request to the '/get_time' route
        with app.test_client() as client:
            response = client.get('/get_time')

            # Assert that the response status code is 200
            self.assertEqual(response.status_code, 200)

            # Assert that the response data matches the expected server time
            self.assertEqual(response.get_json(), 1634567890)

            # Add additional assertions to cover edge cases, such as handling HTTP errors
            # ...

if __name__ == '__main__':
    unittest.main()
