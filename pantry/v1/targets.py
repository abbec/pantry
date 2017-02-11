import flask
import jsonschema

import pantry.common.pantry_error as perror
import pantry.v1.backend as backend

targets_blueprint = flask.Blueprint("targets", __name__)


@targets_blueprint.route('/targets/', methods=['GET'])
def list_targets():
    return flask.jsonify(
        {"targets": backend.get_targets(flask.request.args)})


@targets_blueprint.route('/targets/<int:target_id>/', methods=['GET'])
def get_target(target_id):

    result = backend.get_target(target_id, flask.request.args)

    if not result:
        raise perror.PantryError(
            "Could not find target with id {}".format(target_id),
            status_code=404)

    print(result)

    return flask.jsonify(result)


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

    # construct response with correct location header
    target_id = backend.create_target(content)

    r = flask.jsonify(backend.get_target(target_id))
    r.headers['Location'] = "/targets/{}".format(target_id)
    r.status_code = 201

    return r


@targets_blueprint.route('/targets/<int:target_id>/', methods=['DELETE'])
def delete_target(target_id):

    result = backend.delete_target(target_id)
    if not result:
        raise perror.PantryError(
            f"Could not find target with id {target_id}",
            status_code=404)

    return "", 204
