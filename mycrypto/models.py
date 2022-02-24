from datetime import datetime
from sqlalchemy.sql.schema import ForeignKey
from mycrypto import db, login_manager
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(20), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default="/static/assets/media/avatars/blank.png")
    password = db.Column(db.String(60), nullable=False)

    fav = db.relationship("WatchList", backref="author", lazy=True)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer('5791628bb0b13ce0c676dfde280ba245', expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer('5791628bb0b13ce0c676dfde280ba245')
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.id}', '{self.image_file}')"

class WatchList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    coin_id = db.Column(db.String(100),unique=True, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id",ondelete="CASCADE"), nullable=True)

    def __repr__(self):
        return f"WatchList('{self.id}', '{self.coin_id}')"