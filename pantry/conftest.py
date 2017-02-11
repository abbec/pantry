import pytest
import pantry
import pantry.v1.backend as be


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
def backend(app, request):  # pylint:disable=W0621

    be.init(app)
    be.db.create_all()

    def finalize():
        be.clear()

    request.addfinalizer(finalize)

    return be
