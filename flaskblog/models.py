from datetime import datetime
from flask import current_app
from flaskblog import db, login_manager
from flask_login import UserMixin  # for login manager to work
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


@login_manager.user_loader  # for login manager
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):  # user table
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False,
                           default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    # Post refers to class post
    posts = db.relationship('Post', backref='author', lazy=True)

    def get_reset_token(self, expire_sec=1800):
        s = Serializer(current_app.config["SECRET_KEY"], expire_sec)
        token = s.dumps({"user_id": self.id}).decode('utf-8')

        return token

    @staticmethod  # doesn't take self as arg
    def verify_reset_token(token):
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):  # print(user_instance) will print the string returned
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(200), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.id'), nullable=False)  # user.id is tablename.column

