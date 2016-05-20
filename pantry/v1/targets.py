import flask

import pantry.db.targets as targetsdb
from pantry.db import db as database

from pantry.common.api_common import get_columns
import pantry.common.pantry_error as perror

targets_blueprint = flask.Blueprint("targets", __name__)


@targets_blueprint.route('/targets/', methods=['GET'])
def list_targets():

    # todo: add filtering
    wanted_columns = get_columns(flask.request.args, targetsdb.targets_table.c)

    result = database.engine.execute(database.select(wanted_columns))

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
