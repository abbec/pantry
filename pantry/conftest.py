import pytest
import pantry
from pantry.db import db as database


@pytest.fixture()
def app(request):
    application = pantry.create_app('pantry-testing.cfg')
    application.config['TESTING'] = True

    ctx = application.app_context()
    ctx.push()

    def finalize():
        ctx.pop()

    request.addfinalizer(finalize)

    return application


@pytest.fixture()
def db(app, request):  # pylint:disable=W0621

    database.init_app(app)
    database.create_all()

    def finalize():
        database.reflect()
        database.drop_all()

    request.addfinalizer(finalize)

    return database
