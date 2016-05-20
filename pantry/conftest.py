import pytest
import pantry
from pantry.db import db as database

@pytest.fixture()
def app(request):
    app = pantry.create_app('pantry-testing.cfg')
    app.config['TESTING'] = True

    ctx = app.app_context()
    ctx.push()

    def finalize():
        ctx.pop()

    request.addfinalizer(finalize)

    return app

@pytest.fixture()
def db(app, request):

    database.init_app(app)
    database.create_all()

    def finalize():
        database.reflect()
        database.drop_all()

    request.addfinalizer(finalize)

    return database
