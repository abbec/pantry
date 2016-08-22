import flask

import pantry.db.targets as targetsdb
from pantry.db import db as database

from pantry.common.api_common import (expr_to_query,
                                      filter_columns, reserved_params)
import pantry.common.pantry_error as perror

import jsonschema

targets_blueprint = flask.Blueprint("targets", __name__)


@targets_blueprint.route('/targets/', methods=['GET'])
def list_targets():

    default_cols = [targetsdb.targets_table,
                    targetsdb.tags_table.c.key,
                    targetsdb.tags_table.c.value]

    cols = get_columns(flask.request.args, default_cols)

    q = database.select(cols)
    q = q.select_from(database.join(
        targetsdb.targets_table,
        targetsdb.tags_table,
        isouter=True))

    # filter standard columns
    q = filter_columns(flask.request.args, q,
                       [targetsdb.targets_table.c.hostname,
                        targetsdb.targets_table.c.nickname,
                        targetsdb.targets_table.c.health_percent])

    # filter tags
    q = filter_tags(q, flask.request.args)

    result = database.engine.execute(q).fetchall()
    return flask.jsonify(targets_to_dict(result, force_list=True))


@targets_blueprint.route('/targets/<int:target_id>/', methods=['GET'])
def get_target(target_id):

    default_cols = [targetsdb.targets_table,
                    targetsdb.tags_table.c.key,
                    targetsdb.tags_table.c.value]

    cols = get_columns(flask.request.args, default_cols)

    q = database.select(cols)
    q = q.select_from(targetsdb.targets_table.outerjoin(targetsdb.tags_table))
    q = q.where(targetsdb.targets_table.c.target_id == target_id)

    result = database.engine.execute(q).fetchall()
    if not result:
        raise perror.PantryError(
            "Could not find target with id {}".format(target_id),
            status_code=404)

    target = targets_to_dict(result)
    print(target)
    return flask.jsonify(target)


@targets_blueprint.route('/targets/', methods=['POST'])
def create_target():

    json_schema = {
        "$schema": "http://json-schema.org/draft-04/schema#",
        "type": "object",
        "properties": {
            "hostname": {
                "type": "string"
                },
            "nickname": {
                "type": "string"
                },
            "description": {
                "type": "string"
                },
            "maintainer": {
                "type": "string"
                },
            "healthPercent": {
                "type": "number"
                },
            "state": {
                "type": "string",
                "enum": [
                    "ready",
                    "leased",
                    "down",
                    "maintenance"
                    ]
                },
            "tags": {
                "type": "array"
                }
            },
        "required": [
            "hostname",
            "description",
            "maintainer"
            ]
        }

    content = flask.request.get_json(force=True)

    # validate the provided json
    try:
        jsonschema.validate(content, json_schema)
    except jsonschema.ValidationError as e:
        raise perror.PantryError("invalid data: {}".format(e.message),
                                 status_code=400)

    # create database row, parsing explicitly to not
    # rely on names in JSON
    db_target = {
        "hostname": content['hostname'],
        "description": content['description'],
        "maintainer": content['maintainer'],
        }

    if 'nickname' in content:
        db_target['nickname'] = content['nickname']

    if 'healthPercent' in content:
        db_target['health_percent'] = content['healthPercent']

    if 'state' in content:
        db_target['state'] = content['state']

    # insert target
    q = targetsdb.targets_table.insert(db_target)
    result = database.engine.execute(q)

    target_id = result.inserted_primary_key[0]

    # tags
    if 'tags' in content:
        tq = targetsdb.tags_table.insert()
        db_tags = []
        for tag in content['tags']:
            db_tag = {
                "key": tag['key'],
                "value": tag['value'],
                "target_id": target_id
                }
            db_tags.append(db_tag)

        if len(db_tags) > 0:
            database.engine.execute(tq, db_tags)

    # fetch target again to return it
    j = targetsdb.targets_table.join(targetsdb.tags_table)
    q = database.select([targetsdb.targets_table, targetsdb.tags_table.c.key,
                         targetsdb.tags_table.c.value]).select_from(j).where(
                             targetsdb.targets_table.c.target_id == target_id)

    result = database.engine.execute(q).fetchall()

    # construct response with correct location header
    r = flask.jsonify(targets_to_dict(result))
    r.headers['Location'] = "/targets/{}".format(target_id)
    r.status_code = 201

    return r


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


def targets_to_dict(db_targets, force_list=False):

    targets = {}

    for t in db_targets:
        if t.target_id not in targets:
            target = targets[t.target_id] = {"id": t.target_id}

            if 'hostname' in t:
                target['hostname'] = t.hostname

            if 'description' in t:
                target['description'] = t.description

            if 'maintainer' in t:
                target['maintainer'] = t.maintainer

            if 'health_percent' in t:
                target['healthPercent'] = t.health_percent

            if "key" in t and "value" in t:
                target['tags'] = []

        if "key" in t and "value" in t and t.key is not None:
            target['tags'].append(
                {"key": t.key, "value": t.value})

    if len(targets) > 1 or force_list:
        return {"targets": list(targets.values())}
    elif len(targets) == 1:
        return list(targets.values())[0]

    return targets


def filter_tags(q, args):
    for k, v in args.to_dict().items():
        if k not in reserved_params and k not in targetsdb.targets_table.c:
            q = q.where(targetsdb.tags_table.c.key == k)
            q = expr_to_query(q, targetsdb.tags_table.c.value, v)

    return q


def get_columns(parameters, default):

    fields = parameters.get('fields', None)

    if not fields:
        return default

    fields = fields.split(",")

    filtered_cols = []
    if 'tags' in fields:
        filtered_cols.append(targetsdb.tags_table.c.key)
        filtered_cols.append(targetsdb.tags_table.c.value)

    if 'hostname' in fields:
        filtered_cols.append(targetsdb.targets_table.c.hostname)

    if 'id' not in fields:
        filtered_cols.append(targetsdb.targets_table.c.target_id)

    return filtered_cols
