from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_manager
from flask_migrate import Migrate
from flask_mail import Mail


app = Flask(__name__)
app.config["SECRET_KEY"] = "5791628bb0b13ce0c676dfde280ba245"

##Add your db seetings here
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql://rootuser-here:password-here@localhost/dbname-here"

db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"

app.config["MAIL_SERVER"] = "smtp.googlemail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True

##Please change
app.config["MAIL_USERNAME"] = "rayiszafar@gmail.com"
##Please change
app.config["MAIL_PASSWORD"] = "wzknjhbulyuzrjop"


mail = Mail(app)
from mycrypto import routes
