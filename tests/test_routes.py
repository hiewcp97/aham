import sys
import os
import unittest
import json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app
from test_utils import setup_test_database, clear_test_database

class TestFundsAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up the test client and clear the database."""
        db_path = 'test_funds.db'
        test_config = {
            'TESTING': True,
            'SQLALCHEMY_DATABASE_URI': f'sqlite:///{db_path}',
            'SQLALCHEMY_TRACK_MODIFICATIONS': False
        }
        app = create_app(test_config)
        cls.client = app.test_client()
        cls.client.testing = True
        setup_test_database()  # Clear the database before running tests

    @classmethod
    def tearDownClass(cls):
        """Clear the test database after all tests."""
        clear_test_database()

    def test_create_fund_success(self):
        """Test creating a fund with valid input."""
        response = self.client.post('/funds', json={
            "name": "Test Fund",
            "manager_name": "John Doe",
            "description": "A test fund",
            "nav": 100.0,
            "creation_date": "2025-04-14",
            "performance": 5.0
        })
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn("fund_id", data)
        self.assertEqual(data["name"], "Test Fund")

    def test_create_fund_invalid_input(self):
        """Test creating a fund with missing fields."""
        response = self.client.post('/funds', json={
            "name": "Incomplete Fund"
        })
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn("error", data)
        self.assertEqual(data["error"], "All fields are required.")

    def test_get_fund_success(self):
        """Test retrieving a fund by ID."""
        # First, create a fund
        create_response = self.client.post('/funds', json={
            "name": "Test Fund",
            "manager_name": "John Doe",
            "description": "A test fund",
            "nav": 100.0,
            "creation_date": "2025-04-14",
            "performance": 5.0
        })
        fund_id = create_response.get_json()["fund_id"]

        # Retrieve the fund
        response = self.client.get(f'/funds/{fund_id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["name"], "Test Fund")

    def test_get_fund_not_found(self):
        """Test retrieving a fund that does not exist."""
        response = self.client.get('/funds/nonexistent-id')
        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertIn("error", data)
        self.assertEqual(data["error"], "Fund with ID nonexistent-id not found.")

    def test_update_fund_performance_success(self):
        """Test updating the performance of an existing fund."""
        # First, create a fund
        create_response = self.client.post('/funds', json={
            "name": "Test Fund",
            "manager_name": "John Doe",
            "description": "A test fund",
            "nav": 100.0,
            "creation_date": "2025-04-14",
            "performance": 5.0
        })
        fund_id = create_response.get_json()["fund_id"]

        # Update the performance
        response = self.client.put(f'/funds/{fund_id}', json={"performance": 10.0})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["performance"], 10.0)

    def test_update_fund_performance_invalid_input(self):
        """Test updating a fund's performance with invalid input."""
        # First, create a fund
        create_response = self.client.post('/funds', json={
            "name": "Test Fund",
            "manager_name": "John Doe",
            "description": "A test fund",
            "nav": 100.0,
            "creation_date": "2025-04-14",
            "performance": 5.0
        })
        fund_id = create_response.get_json()["fund_id"]

        # Attempt to update with invalid input
        response = self.client.put(f'/funds/{fund_id}', json={})
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn("error", data)
        self.assertEqual(data["error"], "Invalid input. 'performance' field is required.")

    def test_delete_fund_success(self):
        """Test deleting an existing fund."""
        # First, create a fund
        create_response = self.client.post('/funds', json={
            "name": "Test Fund",
            "manager_name": "John Doe",
            "description": "A test fund",
            "nav": 100.0,
            "creation_date": "2025-04-14",
            "performance": 5.0
        })
        fund_id = create_response.get_json()["fund_id"]

        # Delete the fund
        response = self.client.delete(f'/funds/{fund_id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["message"], "Fund deleted successfully")

    def test_delete_fund_not_found(self):
        """Test deleting a fund that does not exist."""
        fund_id = "nonexistent-id"
        response = self.client.delete(f'/funds/{fund_id}')
        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertIn("error", data)
        self.assertEqual(data["error"], f"Fund with ID {fund_id} not found.")

if __name__ == '__main__':
    unittest.main()