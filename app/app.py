# -*- coding:utf-8 -*-
import os
import sys
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)

from flask import Flask
from flask import render_template
from {{app}}.extensions import db, login_manager, cache, sentry
from flask.sessions import SessionInterface
from beaker.middleware import SessionMiddleware

__all__ = ['create_app']


class SessionInterface(SessionInterface):
    def open_session(self, app, request):
        session = request.environ['{{app}}.session']
        return session

    def save_session(self, app, session, response):
        session.save()


def create_app(config_obj='config.ProductionConfig'):
    app = Flask(__name__, static_url_path="", static_folder="static")
    configure_app(app, config_obj)
    configure_extensions(app)
    configure_blueprints(app)
    configure_jinja(app)
    configure_filter(app)
    configure_error_handlers(app)
    return app


def configure_blueprints(app):
    from {{app}}.resources import resource_blueprints
    blueprints = resource_blueprints
    for blueprint in blueprints:
        app.register_blueprint(blueprint)


def configure_app(app, config_obj='config.ProductionConfig'):
    app.config.from_object(config_obj)


def configure_extensions(app):

    # sentry
    if app.config.get('SENTRY_DSN', None):
        sentry.init_app(app=app,
                        dsn=app.config['SENTRY_DSN'])

    # flask-sqlalchemy
    db.init_app(app)
    with app.app_context():
        db.create_all()

    # flask-login
    login_manager.login_view = "/admin/user/login"
    login_manager.init_app(app)

    # flask-cache
    cache.init_app(app)

    @login_manager.user_loader
    def load_user(token):
        from {{app}}.models import User
        return User.get_from_token(token)

    session_opts = {
        'session.type': 'ext:database',
        'session.url': app.config['SQLALCHEMY_DATABASE_URI'],
        'session.cookie_expires': True,
        'session.auto': True,
        'session.httponly': True,
        'session.secure': True,
        'session.timeout': 3600,
        'session.key': 'meier_session',
        'session.sa.pool_recycle': 250
    }
    app.wsgi_app = SessionMiddleware(app.wsgi_app, session_opts)
    app.session_interface = SessionInterface()


def configure_error_handlers(app):
    @app.errorhandler(401)
    def unauthorized(error):
        return render_template("/errors/error.html", status_code=401), 401

    @app.errorhandler(403)
    def forbidden(error):
        return render_template("/errors/error..html", status_code=403), 403

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template("/errors/error.html", status_code=404), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return render_template("/errors/error.html", status_code=500), 500


def configure_jinja(app):
    app.jinja_env.trim_blocks = True
    app.jinja_env.lstrip_blocks = True


def configure_filter(app):
    pass
