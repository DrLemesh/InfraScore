import pytest
from sqlalchemy import text
from app import db, app

def test_db_connection(client):
    """Test that the app can connect to the database."""
    try:
        # Simple query to check connection
        result = db.session.execute(text("SELECT 1"))
        assert result.scalar() == 1
    except Exception as e:
        pytest.fail(f"Database connection failed: {e}")

def test_user_table_exists(client):
    """Test that the User table has been created."""
    # This verifies db.create_all() worked in conftest
    from app import User
    
    with app.app_context():
        # Verify we can query the table (it should be empty in a fresh test DB)
        assert User.query.count() == 0
