from flask import Blueprint, request, jsonify, current_app, render_template, redirect, url_for, flash
from flask_cors import CORS
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation
from flask_login import current_user, login_user, logout_user
from .models import db, User, Post
from .forms import PostForm

routes = Blueprint('routes', __name__)
CORS(routes)

@routes.route('/', methods=['GET', 'POST'])
def index():
    print(f"Is user authenticated? {current_user.is_authenticated}")
    if request.method == 'POST':  # Handle login form submission
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()

        print(f"Email: {email}, Password: {password}")
        print(f"User found: {user}")

        if user and user.check_password(password):
            access_token = create_access_token(identity=str(user.id))
            flash('Login successful!', 'success')  # Success message
            return redirect(url_for('routes.index'))
        else:
            flash('Invalid email or password.', 'danger')  # Error message

    return render_template('index.html', is_authenticated=current_user.is_authenticated)

@routes.route('/favicon.ico')
def favicon():
    return '', 204

@routes.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # Validate input
        if not username or not email or not password:
            return jsonify({'error': 'All fields are required.'}), 400

        # Check if the email is already registered
        if User.query.filter_by(email=email).first():
            return jsonify({'error': 'The email is already registered.'}), 400

        # Create a new user
        try:
            new_user = User(username=username, email=email)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()

            return jsonify({'message': 'Registration successful!', 'redirect_url': url_for('routes.login')}), 200
        except Exception as e:
            print(f"Error during registration: {e}")
            return jsonify({'error': 'An unexpected error occurred.'}), 500

    return render_template('register.html')


def redirect_with_flash(message, category, endpoint):
    """Helper function to redirect with a flash message."""
    flash(message, category)
    return redirect(url_for(endpoint))

@routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            login_user(user)  # Log in the user
            access_token = create_access_token(identity=str(user.id))
            print(f"Generated Access Token: {access_token}")  # Debugging
            return jsonify({
                'message': 'Login successful!',
                'access_token': access_token,
                'redirect_url': url_for('routes.posts')
            }), 200
        else:
            return jsonify({'error': 'Invalid email or password'}), 401

    return render_template('login.html')

@routes.route('/logout', methods=['GET'])
def logout():
    logout_user()  # Log out the user
    flash('You have been logged out.', 'success')
    return redirect(url_for('routes.login'))  # Redirect to the login page

@routes.route('/create_post', methods=['GET', 'POST'])
def create_post():
    if request.method == 'POST':
        @jwt_required()
        def handle_post():
            current_user_id = get_jwt_identity()
            title = request.json.get('title')
            description = request.json.get('description')
            price = request.json.get('price')
            location = request.json.get('location')
            image_url = request.json.get('image_url') or '/static/images/house-30.png'  # Use a hardcoded path

            print(url_for('static', filename='images/house-30.png'))

            if not title or not description or not price or not location:
                return jsonify({'error': 'All fields except image URL are required'}), 400

            new_post = Post(
                title=title,
                description=description,
                price=price,
                location=location,
                image_url=image_url,
                user_id=current_user_id
            )
            db.session.add(new_post)
            db.session.commit()

            return jsonify({'message': 'Post created successfully!'}), 201

        return handle_post()

    return render_template('create_post.html')

@routes.route('/posts', methods=['GET'])
def posts():
    print(f"Current user: {current_user}")
    print(f"Is user authenticated? {current_user.is_authenticated}")
    posts = Post.query.all()

    # Add a default image URL for posts without an image
    for post in posts:
        if not post.image_url:
            post.image_url = '/static/images/house-30.png'  # Use a hardcoded path

    return render_template('posts.html', posts=posts)

# Get all posts (for all users)
@routes.route('/posts', methods=['GET'])
def get_all_posts():
    # Get query parameters
    location = request.args.get('location')
    min_price = request.args.get('min_price', type=int)
    max_price = request.args.get('max_price', type=int)
    title = request.args.get('title')

    # Build the query
    query = Post.query
    if location:
        query = query.filter(Post.location.ilike(f"%{location}%"))
    if min_price is not None:
        query = query.filter(Post.price >= min_price)
    if max_price is not None:
        query = query.filter(Post.price <= max_price)
    if title:
        query = query.filter(Post.title.ilike(f"%{title}%"))

    # Execute the query
    posts = query.all()
    posts_list = [{
        'id': post.id,
        'title': post.title,
        'description': post.description,
        'price': post.price,
        'location': post.location,
        'image_url': post.image_url,
        'username': post.user.username  # Include the username of the post creator
    } for post in posts]
    return jsonify(posts_list), 200

# Get posts for the logged-in user
@routes.route('/user/posts', methods=['GET'])
@jwt_required()
def get_user_posts():
    current_user_id = get_jwt_identity()
    posts = Post.query.filter_by(user_id=current_user_id).all()
    posts_list = [{
        'id': post.id,
        'title': post.title,
        'description': post.description,
        'price': post.price,
        'location': post.location,
        'image_url': post.image_url,
        'username': post.user.username  # Include the username of the logged-in user
    } for post in posts]
    return jsonify(posts_list), 200

# Add a new post
@routes.route('/add_post', methods=['POST'])
@jwt_required()
def add_post():
    current_user_id = get_jwt_identity()
    title = request.json.get('title')
    description = request.json.get('description')
    price = request.json.get('price')
    location = request.json.get('location')
    image_url = request.json.get('image_url') or '/static/images/house-30.png'  # Use a hardcoded path

    if not title or not description or not price or not location:
        return jsonify({'error': 'All fields are required'}), 400

    new_post = Post(
        title=title,
        description=description,
        price=price,
        location=location,
        image_url=image_url,
        user_id=current_user_id
    )
    db.session.add(new_post)
    db.session.commit()

    return jsonify({'message': 'Post created successfully'}), 201

# Get a single post by ID
@routes.route('/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    post = Post.query.get_or_404(post_id)
    post_data = {
        'id': post.id,
        'title': post.title,
        'description': post.description,
        'price': post.price,
        'location': post.location,
        'image_url': post.image_url,
        'username': post.user.username,  # Include the username of the post creator
        'user_id': post.user_id
    }
    return jsonify(post_data), 200

# Update an existing post
@routes.route('/posts/<int:post_id>', methods=['PUT'])
@jwt_required()
def update_post(post_id):
    try:
        post = Post.query.get_or_404(post_id)
        current_user_id = int(get_jwt_identity())  # Ensure user ID is an integer

        # Check if the logged-in user owns the post
        if post.user_id != current_user_id:
            return jsonify({'error': 'Unauthorized to update this post'}), 403

        # Validate input using PostForm
        form = PostForm(data=request.json)
        if not form.validate():
            return jsonify({'error': 'Invalid input', 'details': form.errors}), 400

        # Update the post
        post.title = form.title.data or post.title
        post.description = form.description.data or post.description
        post.price = form.price.data or post.price
        post.location = form.location.data or post.location
        post.image_url = form.image_url.data or post.image_url
        db.session.commit()

        return jsonify({'message': 'Post updated successfully'}), 200
    except Exception as e:
        current_app.logger.error(f"Error updating post: {e}")
        return jsonify({'error': 'Internal server error'}), 500

# Delete a post
@routes.route('/posts/<int:post_id>', methods=['DELETE'])
@jwt_required()
def delete_post(post_id):
    try:
        post = Post.query.get_or_404(post_id)
        current_user_id = int(get_jwt_identity())  # Ensure user ID is an integer

        # Check if the logged-in user owns the post
        if post.user_id != current_user_id:
            return jsonify({'error': 'Unauthorized to delete this post'}), 403

        db.session.delete(post)
        db.session.commit()

        return jsonify({'message': 'Post deleted successfully'}), 200
    except Exception as e:
        current_app.logger.error(f"Error deleting post: {e}")
        return jsonify({'error': 'Internal server error'}), 500