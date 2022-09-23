from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
db = SQLAlchemy()
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'jsjfvb23456789954345'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    from .dbModels import User
    @login_manager.user_loader
    def load_user(userId):
        return User.query.get(int(userId))
    from .auth import auth as authBluePrint
    app.register_blueprint(authBluePrint)

    from .main import main as mainBluePrint
    app.register_blueprint(mainBluePrint)


    return app