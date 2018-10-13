import os
basedir = os.path.abspath(os.path.dirname(__file__))

# Config object with all settings
class Config(object):
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will_never__guess'
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
	SQLALCHEMY_TRACK_MODIFICATIONS = False