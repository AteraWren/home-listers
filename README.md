# Home Listers

Home Listers is a web application for listing and managing property posts. Users can register, log in, create posts, and manage their own listings.

## Features

- User authentication (register, login, logout)
- Create, view, and delete property posts
- Placeholder image for posts without an image URL
- Responsive design for all devices

## Live Demo

The app is live on Render: [Home Listers](https://home-listers.onrender.com)

## Technologies Used

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Database**: PostgreSQL (via Supabase)
- **Deployment**: Render

## Installation

### Prerequisites

- Python 3.10 or higher
- Virtual environment (optional but recommended)

### Steps

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/home-listers.git
   cd home-listers
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/Scripts/activate  # On Windows
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up the environment variables:

   - Create a `.env` file in the root directory and add the following:
     ```plaintext
     DATABASE_URL=your_database_url
     SECRET_KEY=your_secret_key
     JWT_SECRET_KEY=your_jwt_secret_key
     ```

5. Set up the database:

   - Run the migrations to create the necessary tables:
     ```bash
     flask db upgrade
     ```

6. Run the app:

   ```bash
   flask run
   ```

7. Open the app in your browser:
   ```
   http://127.0.0.1:5000
   ```

## Deployment

### Deploying on Render

1. Push your code to GitHub.
2. Create a new **Web Service** on Render.
3. Use the following start command in your `Procfile`:
   ```plaintext
   web: gunicorn -w 4 -b 0.0.0.0:$PORT backend.run:app
   ```
4. Add the required environment variables (`DATABASE_URL`, `SECRET_KEY`, `JWT_SECRET_KEY`) in Render's **Environment** settings.
5. Deploy the app and access it at the provided Render URL.

Caution!: The app takes about 30 seconds to use the beginning of the app to spin up due to being free on render! Please give it some time!

## License

This project is licensed under the MIT License.
