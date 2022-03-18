import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy  # ORM
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flaskblog.config import Config


mail = Mail()
db = SQLAlchemy()  # db instance
bcrypt = Bcrypt()  # for hashing passwords
login_manager = LoginManager() # for login system
login_manager.login_view = 'users.login' # login route(same as url_for arg)
login_manager.login_message_category = 'info' # changing flash message

# before blueprints: from flaskblog import routes # preventing circular import by placing this line here


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config) # takes config from Config
    
    mail.init_app(app) # mail
    db.init_app(app) #  database
    bcrypt.init_app(app) # hashing
    login_manager.init_app(app) # login management

    from flaskblog.users.routes import users
    from flaskblog.posts.routes import posts
    from flaskblog.main.routes import main
    from flaskblog.errors.handlers import errors

    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app
