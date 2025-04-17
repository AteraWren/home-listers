def test_register_user(client):
    # Test successful registration
    response = client.post('/register', data={
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'password123'
    })
    assert response.status_code == 200
    assert b'Registration successful!' in response.data

    # Test registration with missing fields
    response = client.post('/register', data={
        'username': '',
        'email': 'testuser2@example.com',
        'password': 'password123'
    })
    assert response.status_code == 400
    assert b'All fields are required.' in response.data

    # Test registration with duplicate email
    response = client.post('/register', data={
        'username': 'testuser2',
        'email': 'testuser@example.com',  # Duplicate email
        'password': 'password123'
    })
    assert response.status_code == 400
    assert b'The email is already registered.' in response.data

def test_login_user(client):
    # Create a test user
    client.post('/register', data={
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'password123'
    })

    # Test successful login
    response = client.post('/login', data={
        'email': 'testuser@example.com',
        'password': 'password123'
    })
    assert response.status_code == 200
    assert b'Login successful!' in response.data

    # Test login with invalid password
    response = client.post('/login', data={
        'email': 'testuser@example.com',
        'password': 'wrongpassword'
    })
    assert response.status_code == 401
    assert b'Invalid email or password' in response.data

    # Test login with non-existent email
    response = client.post('/login', data={
        'email': 'nonexistent@example.com',
        'password': 'password123'
    })
    assert response.status_code == 401
    assert b'Invalid email or password' in response.data