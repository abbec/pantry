# import all endpoints here and register below
from pantry.v1 import targets
from pantry.v1 import leases


def register_api(app, url_prefix):
    app.register_blueprint(targets.targets_blueprint, url_prefix=url_prefix)
    app.register_blueprint(leases.leases_blueprint, url_prefix=url_prefix)
