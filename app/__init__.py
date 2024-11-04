# app/__init__.py

from flask import Flask

def create_app():
    # Create the Flask application instance
    app = Flask(__name__, template_folder='../templates', static_folder='../static')

    # Optional: Additional configurations can go here
    # e.g., app.config['SECRET_KEY'] = 'your_secret_key'

    # Import the main blueprint
    from .routes import main
    
    # Register the blueprint with the application
    app.register_blueprint(main)

    return app

# Create an instance of the app when the module is imported
app = create_app()