def test_create_post(client):
    # Register and log in a test user
    client.post('/register', data={
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'password123'
    })
    login_response = client.post('/login', data={
        'email': 'testuser@example.com',
        'password': 'password123'
    })
    access_token = login_response.get_json()['access_token']

    # Test successful post creation
    response = client.post('/create_post', json={
        'title': 'Test Post',
        'description': 'This is a test post.',
        'price': 100,
        'location': 'Test City',
        'image_url': 'https://example.com/image.jpg'
    }, headers={'Authorization': f'Bearer {access_token}'})
    assert response.status_code == 201
    assert b'Post created successfully!' in response.data

    # Test post creation without authentication
    response = client.post('/create_post', json={
        'title': 'Unauthorized Post',
        'description': 'This should fail.',
        'price': 50,
        'location': 'Unauthorized City',
        'image_url': 'https://example.com/image.jpg'
    })
    assert response.status_code == 401
    assert b'Missing Authorization Header' in response.data

def test_get_posts(client):
    # Register and log in a test user
    client.post('/register', data={
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'password123'
    })
    login_response = client.post('/login', data={
        'email': 'testuser@example.com',
        'password': 'password123'
    })
    access_token = login_response.get_json()['access_token']

    # Create a test post
    client.post('/create_post', json={
        'title': 'Test Post',
        'description': 'This is a test post.',
        'price': 100,
        'location': 'Test City',
        'image_url': 'https://example.com/image.jpg'
    }, headers={'Authorization': f'Bearer {access_token}'})

    # Retrieve all posts
    response = client.get('/posts')
    assert response.status_code == 200
    assert b'Test Post' in response.data

def test_delete_post(client):
    """
    Test the deletion of a post.

    This test verifies that a user can delete their own post and that attempting
    to delete the same post again returns a 404 error.

    Args:
        client (FlaskClient): The test client for making HTTP requests.

    Returns:
        None
    """
    # Register and log in a test user
    client.post('/register', data={
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'password123'
    })
    login_response = client.post('/login', data={
        'email': 'testuser@example.com',
        'password': 'password123'
    })
    access_token = login_response.get_json()['access_token']

    # Create a test post
    create_response = client.post('/create_post', json={
        'title': 'Test Post',
        'description': 'This is a test post.',
        'price': 100,
        'location': 'Test City',
        'image_url': 'https://example.com/image.jpg'
    }, headers={'Authorization': f'Bearer {access_token}'})
    response_data = create_response.get_json()
    assert 'id' in response_data, "Response does not contain 'id'"
    post_id = response_data['id']

    # Delete the post
    response = client.delete(f'/posts/{post_id}', headers={'Authorization': f'Bearer {access_token}'})
    assert response.status_code == 200
    assert b'Post deleted successfully' in response.data

    # Attempt to delete the post again
    response = client.delete(f'/posts/{post_id}', headers={'Authorization': f'Bearer {access_token}'})
    assert response.status_code == 404
    assert b'Post not found' in response.data