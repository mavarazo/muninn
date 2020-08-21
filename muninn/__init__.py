import os

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_moment import Moment

from config import Config

db = SQLAlchemy()
migrate = Migrate()
moment = Moment()

def create_app(config_class=Config):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    moment.init_app(app)

    from . import dashboard
    app.register_blueprint(dashboard.bp)
    app.add_url_rule('/', endpoint='index')

    from . import radio
    app.register_blueprint(radio.bp, url_prefix='/radio')

    from . import jenkins
    app.register_blueprint(jenkins.bp, url_prefix='/jenkins')

    from . import sonarqube
    app.register_blueprint(sonarqube.bp, url_prefix='/sonarqube')

    from . import feed
    app.register_blueprint(feed.bp, url_prefix='/feed')

    return app

from muninn import models

