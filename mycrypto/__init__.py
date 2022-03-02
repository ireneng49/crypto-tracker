from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_manager
from flask_migrate import Migrate
from flask_mail import Mail
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get('SECRET_KEY','hellosecret1')
print('******************')
print('******************')
print('******************')

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://irene:@localhost:5432/crypto"

db = SQLAlchemy(app)
migrate = Migrate(app, db, compare_type=True)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"

app.config["MAIL_SERVER"] = "smtp.googlemail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True


app.config["MAIL_USERNAME"] = "rayiszafar@gmail.com"

app.config["MAIL_PASSWORD"] = "wzknjhbulyuzrjop"


mail = Mail(app)
from mycrypto import routes
