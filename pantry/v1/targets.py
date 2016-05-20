import flask

import pantry.db.targets as targetsdb
from pantry.db import db as database

targets_blueprint = flask.Blueprint("targets", __name__)


@targets_blueprint.route('/targets/', methods=['GET'])
def list_targets():

    # todo: add filtering and field inclusion
    q = targetsdb.targets_table.select()
    result = database.engine.execute(q)

    results = [dict(row) for row in result]

    return flask.jsonify({"targets": results})


@targets_blueprint.route('/targets/<int:target_id>/', methods=['GET'])
def get_target(target_id):
    # todo: add field inclusion
    result = database.engine.execute(
        targetsdb.targets_table.select().where(
            targetsdb.targets_table.c.target_id == target_id))

    results = dict(result.fetchone())
    return flask.jsonify(results)
