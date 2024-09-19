from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


db = SQLAlchemy()
DB_NAME = "database.db"


# Function, 'create_app' is defined to create the Flask app.
# This is imported into app.py which allows the website to run.
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "8I7xAHW8yD"
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
    
    from .views import views
    from .auth import auth
    
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")
    
    from .models import User, Post, Comment, Like
    
    with app.app_context():
        db.create_all()
        print("Created database!")
    
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app