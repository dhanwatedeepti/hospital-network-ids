import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    "super-secret-key-change-this"
    )

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'instance', 'database.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAX_REQUESTS_PER_SECOND = 10
    BRUTE_FORCE_LIMIT = 5