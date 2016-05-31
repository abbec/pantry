import flask

import pantry.db.leases as leasesdb
from pantry.db import db as database
from pantry.common.api_common import get_columns

leases_blueprint = flask.Blueprint("leases", __name__)


@leases_blueprint.route('/leases/', methods=['GET'])
def list_leases():

    # todo: add filtering
    wanted_columns = get_columns(flask.request.args, leasesdb.leases_table.c)

    result = database.engine.execute(database.select(wanted_columns))

    return flask.jsonify({"leases": [dict(row) for row in result]})
