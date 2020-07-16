import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JENKINS_USERNAME = os.environ.get('JENKINS_USERNAME')
    JENKINS_TOKEN = os.environ.get('JENKINS_TOKEN')
    SONARQUBE_TOKEN = os.environ.get('SONARQUBE_TOKEN')
    SONARQUBE_URL_COMPONENT = os.environ.get('SONARQUBE_URL_COMPONENT')