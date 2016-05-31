import logging
import os
import flask
import celery
import werkzeug.contrib.profiler as profiler
from pantry.db import db as database, migrate
from pantry.v1 import register_api as register_api_v1
from pantry.common import pantry_error

# import database schemas
import pantry.db.targets  # noqa


def create_app(cfg_file):
    app = flask.Flask(__name__)
    app.config.from_pyfile(cfg_file)

    if app.debug:
        app.logger.setLevel(logging.DEBUG)

    if 'SQLALCHEMY_DATABASE_URI' not in app.config:
        db_driver = app.config['DB_DRIVER']
        db_dialect = app.config.get('DB_DIALECT', None)
        db_user = app.config.get('DB_USER', None)
        db_password = app.config.get('DB_PASSWORD', None)
        db_host = app.config.get('DB_HOST', None)
        db_name = app.config.get('DB_NAME', None)

        # make path absolute to not confuse alembic
        # this should still work with in-memory dbs
        # since the db name is empty in that case
        if db_driver == "sqlite" and db_name is not None:
            if not os.path.isabs(db_name):
                db_name = os.path.join(app.root_path, db_name)

        app.config['SQLALCHEMY_DATABASE_URI'] = "{}{}://{}{}{}/{}".format(
            db_driver,
            ("+" + db_dialect) if db_dialect is not None else "",
            db_user or "",
            (":" + db_password) if db_password is not None else "",
            ("@" + db_host) if db_host is not None else "",
            db_name or "")

    # set up wanted middleware
    if app.config.get('PROFILE', False):
        app.wsgi_app = profiler.ProfilerMiddleware(
            app.wsgi_app, restrictions=[10])

    # init database
    database.init_app(app)

    # error handling
    app.register_blueprint(pantry_error.pantry_error)

    # database migrations
    migrate.init_app(app, database)

    # register api blueprints
    register_api_v1(app, url_prefix="/api/v1")

    return app


def create_celery(cfg, app=None):

    app = app or create_app(cfg)
    capp = celery.Celery(app.import_name,
                         backend=app.config['CELERY_BACKEND'],
                         broker=app.config['CELERY_BROKER_URL'])

    capp.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def run(self, *args, **kwargs):
            return TaskBase.run(self, *args, **kwargs)

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    capp.Task = ContextTask
    return capp
