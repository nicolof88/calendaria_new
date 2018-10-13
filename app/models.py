from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import datetime


# User Class for ORM
class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(250), index=True, unique=True)
	first_name = db.Column(db.String(250), index=True)
	dob = db.Column(db.DateTime, index=True)
	password_hash = db.Column(db.String(128))

	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)

	def __repr__(self):
		return '<User: {} {} ({})>'.format(self.first_name, self.dob.strftime('%m/%d/%Y'), self.email)
		

# Set the user id to track the user currently online
@login.user_loader
def load_user(id):
	return User.query.get(int(id))