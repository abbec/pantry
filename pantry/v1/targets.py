import flask

import pantry.db.targets as targetsdb
from pantry.db import db as database

targets_blueprint = flask.Blueprint("targets", __name__)


@targets_blueprint.route('/targets/', methods=['GET'])
def list_targets():

    q = targetsdb.targets_table.select()
    result = database.engine.execute(q)

    results = [dict(row) for row in result]

    return flask.jsonify({"targets": results})
