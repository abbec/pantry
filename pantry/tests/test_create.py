import tempfile
import logging
import os
import werkzeug.contrib.profiler as profiler
import pantry


def test_create_debug():
    with tempfile.NamedTemporaryFile(mode='w') as f:
        f.write("DEBUG = True\nDB_DRIVER = 'sqlite'")
        f.flush()

        a = pantry.create_app(f.name)
        assert a.debug
        assert a.logger.level == logging.DEBUG


def test_create_minimal_db_setup():
    with tempfile.NamedTemporaryFile(mode='w') as f:
        f.write("DB_DRIVER = 'sqlite'")
        f.flush()

        a = pantry.create_app(f.name)
        db_driver = a.config.get(
            'SQLALCHEMY_DATABASE_URI',
            None)

        assert db_driver is not None
        assert db_driver == "sqlite:///"


def test_create_sqlite_db_setup():
    with tempfile.NamedTemporaryFile(mode='w') as f:
        f.write("DB_DRIVER = 'sqlite'\n")
        f.write("DB_NAME = 'pantry.db'")
        f.flush()

        a = pantry.create_app(f.name)
        db_driver = a.config.get(
            'SQLALCHEMY_DATABASE_URI',
            None)

        db_name = os.path.join(a.root_path, 'pantry.db')
        assert db_driver is not None
        assert db_driver == "sqlite:///{}".format(db_name)


def test_create_profile():
    with tempfile.NamedTemporaryFile(mode='w') as f:
        f.write("PROFILE = True\nDB_DRIVER = 'sqlite'")
        f.flush()

        a = pantry.create_app(f.name)
        assert not a.debug
        assert isinstance(a.wsgi_app, profiler.ProfilerMiddleware)


def test_create_celery(app):
    celery = pantry.create_celery('bogus', app)

    assert celery is not None
