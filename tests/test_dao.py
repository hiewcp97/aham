import sys
import os
import unittest
import uuid

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.dao import add_fund, get_all_funds, get_fund_by_id, update_fund_performance, delete_fund
from app.dto import InvestmentFund
from test_utils import setup_test_database, clear_test_database

class TestFundsDAO(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up the test database schema once for all tests."""
        setup_test_database()

    @classmethod
    def tearDownClass(cls):
        """Clear the test database after all tests."""
        clear_test_database()

    def test_get_all_funds_with_filters(self):
        # Add multiple funds to the database
        fund1 = InvestmentFund(
            fund_id=str(uuid.uuid4()),
            name="Property Fund",
            manager_name="Alice Johnson",
            description="A property-focused fund",
            nav=150.0,
            creation_date="2025-04-14",
            performance=8.0
        )
        fund2 = InvestmentFund(
            fund_id=str(uuid.uuid4()),
            name="Health Fund",
            manager_name="Bob Smith",
            description="A healthcare-focused fund",
            nav=200.0,
            creation_date="2025-04-14",
            performance=10.0
        )
        fund3 = InvestmentFund(
            fund_id=str(uuid.uuid4()),
            name="Property Growth Fund",
            manager_name="Alice Johnson",
            description="A growth-focused property fund",
            nav=250.0,
            creation_date="2025-04-14",
            performance=12.0
        )
        add_fund(fund1)
        add_fund(fund2)
        add_fund(fund3)

        # Test filtering by name
        filtered_by_name = get_all_funds(name_filter="Property")
        self.assertTrue(all("Property" in fund.name for fund in filtered_by_name))

        # Test filtering by manager_name
        filtered_by_manager = get_all_funds(manager_name_filter="Alice Johnson")
        self.assertTrue(all(fund.manager_name == "Alice Johnson" for fund in filtered_by_manager))

        # Test filtering by both name and manager_name
        filtered_by_both = get_all_funds(name_filter="Property", manager_name_filter="Alice Johnson")
        self.assertTrue(all("Property" in fund.name and fund.manager_name == "Alice Johnson" for fund in filtered_by_both))

    def test_add_and_get_fund(self):
        fund = InvestmentFund(
            fund_id=str(uuid.uuid4()),  # Generate a unique fund_id
            name="Test Fund",
            manager_name="John Doe",
            description="A test fund",
            nav=100.0,
            creation_date="2025-04-14",
            performance=5.0
        )
        add_fund(fund)
        retrieved_fund = get_fund_by_id(fund.fund_id)
        self.assertIsNotNone(retrieved_fund)
        self.assertEqual(retrieved_fund.name, "Test Fund")

    def test_update_fund_performance(self):
        fund = InvestmentFund(
            fund_id=str(uuid.uuid4()),  # Generate a unique fund_id
            name="Another Fund",
            manager_name="Jane Doe",
            description="Another test fund",
            nav=200.0,
            creation_date="2025-04-14",
            performance=10.0
        )
        add_fund(fund)
        update_fund_performance(fund.fund_id, 15.0)
        updated_fund = get_fund_by_id(fund.fund_id)
        self.assertEqual(updated_fund.performance, 15.0)

    def test_delete_fund(self):
        fund = InvestmentFund(
            fund_id=str(uuid.uuid4()),  # Generate a unique fund_id
            name="Delete Fund",
            manager_name="Mark Smith",
            description="Fund to delete",
            nav=300.0,
            creation_date="2025-04-14",
            performance=20.0
        )
        add_fund(fund)
        delete_fund(fund.fund_id)
        deleted_fund = get_fund_by_id(fund.fund_id)
        self.assertIsNone(deleted_fund)

if __name__ == '__main__':
    unittest.main()