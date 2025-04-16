import os
import tempfile
import time

from app.dao import create_table

TEST_DB = 'test_funds.db'

def setup_test_database():
    temp_db = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
    db_path = temp_db.name
    temp_db.close()  # THIS IS IMPORTANT ON WINDOWS
    os.environ['DB'] = db_path
    create_table()

def clear_test_database():
    db_path = os.environ.get('DB')
    if db_path and os.path.exists(db_path):
        try:
            os.remove(db_path)
        except PermissionError:
            time.sleep(0.5)
            try:
                os.remove(db_path)
            except Exception as e:
                print(f"Failed to delete test DB: {e}")