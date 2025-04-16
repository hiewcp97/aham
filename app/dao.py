import sqlite3
import os

from app.dto import InvestmentFund

def get_connection():
    """Helper function to get a database connection."""
    # Use DB environment variable if set, otherwise default to 'funds.db'
    db_path = os.getenv('DB', 'funds.db')
    return sqlite3.connect(db_path)

def create_table():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS funds (
                fund_id TEXT PRIMARY KEY,
                name TEXT,
                manager_name TEXT,
                description TEXT,
                nav REAL,
                creation_date TEXT,
                performance REAL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()

def add_fund(fund):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO funds (fund_id, name, manager_name, description, nav, creation_date, performance)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (fund.fund_id, fund.name, fund.manager_name, fund.description, fund.nav, fund.creation_date, fund.performance))
        conn.commit()

def get_all_funds(name_filter=None, manager_name_filter=None, page=1, per_page=10):
    with get_connection() as conn:
        cursor = conn.cursor()

        # Build the base query
        query = 'SELECT * FROM funds'
        params = []

        # Add filtering conditions if applicable
        if name_filter or manager_name_filter:
            query += ' WHERE'
            conditions = []
            if name_filter:
                conditions.append(' LOWER(name) LIKE ?')
                params.append(f'%{name_filter.lower()}%')
            if manager_name_filter:
                conditions.append(' LOWER(manager_name) LIKE ?')
                params.append(f'%{manager_name_filter.lower()}%')
            query += ' AND'.join(conditions)

        # Add pagination
        offset = (page - 1) * per_page
        query += ' LIMIT ? OFFSET ?'
        params.extend([per_page, offset])

        cursor.execute(query, params)
        rows = cursor.fetchall()
        return [InvestmentFund(*row) for row in rows]

def get_fund_by_id(fund_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM funds WHERE fund_id = ?', (fund_id,))
        row = cursor.fetchone()
        return InvestmentFund(*row) if row else None

def update_fund_performance(fund_id, performance):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('UPDATE funds SET performance = ? WHERE fund_id = ?', (performance, fund_id))
        conn.commit()

def delete_fund(fund_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM funds WHERE fund_id = ?', (fund_id,))
        conn.commit()