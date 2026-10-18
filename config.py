import os

class Config:
    SECRET_KEY = 'cle-secrete-incidents-2024'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///incidents.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
