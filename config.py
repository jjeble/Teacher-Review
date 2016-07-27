WTF_CSRF_ENABLED = True
SECRET_KEY = "you-will-never-guess"
import os
basedir = os.path.abspath(os.path.dirname(__file__))
MAIL_SERVER = 'localhost'
MAIL_PORT = 25
MAIL_USERNAME = None
MAIL_PASSWORD = None

ADMINS = ['jay.kyogre@gmail.com']

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
POSTS_PER_PAGE = 3

