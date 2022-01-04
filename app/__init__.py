from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from app.config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

# db = SQLAlchemy()
# bcrypt = Bcrypt()
# login_manager = LoginManager()

login_manager.login_view = "users.login" ## Rout name For Redirecting user to login page
login_manager.login_message_category = "danger" ## Class name For Redirecting user to login page

##Modules Import
from app.users.routes import users
from app.posts.routes import posts
from app.main.routes import main

## Create Blueprint of Modules
app.register_blueprint(users)
app.register_blueprint(posts)
app.register_blueprint(main)

# def create_app(config_class = Config):
#     app = Flask(__name__)
#     app.config.from_object(Config)

#     db.init_app(app)
#     bcrypt.init_app(app)
#     login_manager.init_app(app)

#     ##Modules Import
#     from app.users.routes import users
#     from app.posts.routes import posts
#     from app.main.routes import main
#     ## Create Blueprint of Modules
#     app.register_blueprint(users)
#     app.register_blueprint(posts)
#     app.register_blueprint(main)

#     return app