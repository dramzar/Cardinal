from cardinal import cardinalEnv
from flask_login import UserMixin

class Users(UserMixin, cardinalEnv.db().Model):
    db = cardinalEnv.db()
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(102), nullable=False)
