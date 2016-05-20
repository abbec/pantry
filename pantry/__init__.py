import logging
import os
import flask
import werkzeug.contrib.profiler as profiler
from pantry.db import db as database, migrate
from pantry.v1 import register_api as register_api_v1

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

    # database migrations
    migrate.init_app(app, database)

    # register api blueprints
    register_api_v1(app, url_prefix="/api/v1")

    return app
