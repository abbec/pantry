import flask

import pantry.db.leases as leasesdb
from pantry.db import db as database

leases_blueprint = flask.Blueprint("leases", __name__)


@leases_blueprint.route('/leases/', methods=['GET'])
def list_leases():

    # todo: add filtering
    # wanted_columns = get_columns(flask.request.args, leasesdb.leases_table.c)

    result = database.engine.execute(database.select(leasesdb.leases_table.c))

    return flask.jsonify({"leases": [dict(row) for row in result]})
