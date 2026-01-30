import pytest
import sys
import os

# Add backend directory to path so we can import app
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db

@pytest.fixture
def client():
    app.config['TESTING'] = True
    # In CI, DATABASE_URL will be provided by the service container
    with app.test_client() as client:
        with app.app_context():
            # Create tables for tests
            db.create_all()
        yield client
        # Clean up is handled by the container being destroyed, 
        # but technically we could db.drop_all() here.
