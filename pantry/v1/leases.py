import flask

# from pantry.db import db

leases_blueprint = flask.Blueprint("leases", __name__)


@leases_blueprint.route('/leases/', methods=['GET'])
def list_leases():
    pass
