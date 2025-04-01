from backend import create_app

app = create_app()

if __name__ == '__main__':
    print("Running in development mode...")
    app.run(debug=True)