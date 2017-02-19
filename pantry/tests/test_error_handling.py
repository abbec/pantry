import json
import flask

import pantry.common.pantry_error


def get_json(response):
    return json.loads(response.get_data(as_text=True))


def test_404(app):

    r = app.test_client().get('/api/v1/nonexistent/')
    data = get_json(r)

    assert r.status_code == 404
    assert "not be found" in data["message"]


def test_internal_error(app):

    @app.route("/raise")
    def fail():
        flask.abort(500)

    r = app.test_client().get('/raise')
    data = get_json(r)

    assert r.status_code == 500
    assert "internal" in data['message']
    del fail


def test_invalid_request(app):

    @app.route("/raise")
    def fail():
        flask.abort(400)

    r = app.test_client().get('/raise')
    data = get_json(r)

    assert r.status_code == 400
    assert "bad" in data['message']
    del fail


def test_pantry_error(app):

    @app.route("/raise")
    def fail():
        raise pantry.common.pantry_error.PantryError("test")

    r = app.test_client().get('/raise')
    data = get_json(r)

    assert r.status_code == 400
    assert "test" in data['message']
    del fail
