import os

class Config:
    SECRET_KEY = 'bc74c9a4138cdabf49be24617d7ac4db'
    # on fs, relative path
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'

    #for email
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
