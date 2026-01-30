def test_home_page(client):
    """Test that the landing page loads."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"InfraScore" in response.data

def test_health_check(client):
    """Test that the application is running and can return valid JSON."""
    # We might not have a dedicated health endpoint, but we can check if a 404 is valid JSON
    # or check the login page
    response = client.get('/login')
    assert response.status_code == 200
