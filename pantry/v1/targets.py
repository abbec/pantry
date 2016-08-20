import flask

import pantry.db.targets as targetsdb
from pantry.db import db as database

from pantry.common.api_common import get_columns, filter_columns
import pantry.common.pantry_error as perror

targets_blueprint = flask.Blueprint("targets", __name__)


@targets_blueprint.route('/targets/', methods=['GET'])
def list_targets():

    # todo: add filtering
    cols = targetsdb.targets_table.c
    wanted_columns = get_columns(flask.request.args, cols)
    q = database.select(wanted_columns)
    q = filter_columns(flask.request.args, q,
                       [cols.hostname, cols.nickname, cols.health_percent])

    # todo: filter tag values

    result = database.engine.execute(q)

    return flask.jsonify({"targets": [dict(row) for row in result]})


@targets_blueprint.route('/targets/<int:target_id>/', methods=['GET'])
def get_target(target_id):

    columns = targetsdb.targets_table.c
    wanted_columns = get_columns(flask.request.args, columns)

    q = database.select(wanted_columns).where(
        columns.target_id == target_id)
    result = database.engine.execute(q).fetchone()

    if not result:
        raise perror.PantryError(
            "Could not find target with id {}".format(target_id),
            status_code=404)

    target = dict(result)
    return flask.jsonify(target)


@targets_blueprint.route('/targets/<int:target_id>/', methods=['DELETE'])
def delete_target(target_id):

    r = database.engine.execute(
        targetsdb.targets_table.delete().
        where(targetsdb.targets_table.c.target_id == target_id))

    if r.rowcount == 0:
        raise perror.PantryError(
            "Could not find target with id {}".format(target_id),
            status_code=404)

    return "", 200
