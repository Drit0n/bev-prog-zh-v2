# app.py
from backend import create_app  # Import the create_app function from the backend module

app = create_app()  # Initialize the Flask app using the factory function

if __name__ == '__main__':
    app.run(debug=True)  # Run the app in development mode