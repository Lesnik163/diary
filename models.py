from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class Users(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key=True)
  login = db.Column(db.String(100), unique=True, nullable=False)
  password = db.Column(db.String(256), nullable=False)

  def __repr__(self):
    return f"Users('{self.login}')"
