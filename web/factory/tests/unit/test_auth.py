def test_login_page_loads(client):
    """Test that login page loads"""
    response = client.get('/auth/login')
    assert response.status_code == 200
    assert b'Login' in response.data

def test_valid_login(client, sample_admin_user):
    """Test login with valid credentials"""
    response = client.post('/auth/login', data={
        'email': 'test@example.com',
        'password': 'testpassword',
        'remember_me': False
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'You have successfully logged in!' in response.data

def test_invalid_login(client, sample_admin_user):
    """Test login with invalid credentials"""
    response = client.post('/auth/login', data={
        'email': 'test@example.com',
        'password': 'wrongpassword',
        'remember_me': False
    }, follow_redirects=True)
    
    assert b'Invalid email or password' in response.data

def test_admin_can_view_messages(authenticated_admin_client, sample_message):
    """Test that admin user can view messages page."""
    # Act
    response = authenticated_admin_client.get('/admin/message/list')

    assert b'Admin - View Messages' in response.data

def test_admin_can_view_users(authenticated_admin_client, sample_admin_user):
    """Test login with valid credentials"""
    response = authenticated_admin_client.get('/admin/user/list')
    
    # assert response.status_code == 200
    assert b'Admin - Manage Users' in response.data

def test_contact_form_submission(client):
    """Test contact form submission"""
    response = client.post('/contact', data={
        'firstname': 'John',
        'lastname': 'Doe',
        'email': 'john@example.com',
        'company': 'Test Corp',
        'message': 'Test message'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Thank you for your message' in response.data