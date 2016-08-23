import json
import flask
import pantry.db.fake as fake
from pantry.db.targets import targets_table


def get_json(response):
    return json.loads(response.get_data(as_text=True))


def test_list(app, db):

    # insert an event
    tgt = fake.create_targets(1)
    db.engine.execute(targets_table.insert(), tgt)

    # fetch and verify
    r = app.test_client().get('/api/v1/targets/')
    data = get_json(r)

    assert len(data['targets']) > 0


def test_list_fields(app, db):

    # insert an event
    tgt = fake.create_targets(1)
    db.engine.execute(targets_table.insert(), tgt)

    # fetch and verify
    r = app.test_client().get('/api/v1/targets/?fields=hostname')
    data = get_json(r)

    assert len(data['targets']) > 0
    assert data['targets'][0]['hostname'] is not None
    assert 'nickname' not in data['targets'][0]


def test_list_filter(app, db):

    # insert an event
    tgt = fake.create_targets(2)
    tgt[0]['hostname'] = "sune"
    tgt[1]['hostname'] = "suna"
    db.engine.execute(targets_table.insert(), tgt)

    # fetch and verify
    r = app.test_client().get('/api/v1/targets/?hostname=sune')
    data = get_json(r)

    assert len(data['targets']) == 1
    assert data['targets'][0]['hostname'] == "sune"


def test_list_filter_arithmetic(app, db):

    # insert an event
    tgt = fake.create_targets(1)
    tgt[0]['health_percent'] = 45
    db.engine.execute(targets_table.insert(), tgt)

    # fetch and verify
    r = app.test_client().get('/api/v1/targets/?health_percent={"gt":45}')
    data = get_json(r)

    assert len(data['targets']) == 0

    r = app.test_client().get('/api/v1/targets/?health_percent={"gte":45}')
    data = get_json(r)

    assert len(data['targets']) == 1

    r = app.test_client().get('/api/v1/targets/?health_percent={"lt":46}')
    data = get_json(r)

    assert len(data['targets']) == 1

    r = app.test_client().get('/api/v1/targets/?health_percent={"lt":45}')
    data = get_json(r)

    assert len(data['targets']) == 0

    r = app.test_client().get('/api/v1/targets/?health_percent={"lte":45}')
    data = get_json(r)

    assert len(data['targets']) == 1


def test_single(app, db):

    # insert an event
    tgt = fake.create_targets(1)
    db.engine.execute(targets_table.insert(), tgt)

    # fetch and verify
    r = app.test_client().get('/api/v1/targets/1/')
    data = get_json(r)

    assert r.status_code == 200
    assert data["hostname"] is not None


def test_create(app, db):

    del db

    target = {
            "hostname": "sune",
            "description": "Awesome host",
            "maintainer": "sune@suneco.biz",
            "healthPercent": 99,
            "tags": [
                {"key": "platform", "value": "linux"},
                {"key": "gpu", "value": "amd"}]
            }

    r = app.test_client().post('/api/v1/targets/', data=json.dumps(target))

    data = get_json(r)
    assert r.status_code == 201
    assert "id" in data
    assert 'Location' in r.headers

    assert data['healthPercent'] == target['healthPercent']
    assert data['hostname'] == target['hostname']

    assert len(data['tags']) == 2


def test_delete(app, db):

    # insert an event
    tgt = fake.create_targets(1)
    db.engine.execute(targets_table.insert(), tgt)

    # fetch and verify
    r = app.test_client().delete('/api/v1/targets/1/')

    assert r.status_code == 200


def test_delete_nonexistent(app, db):

    del db

    # fetch and verify
    r = app.test_client().delete('/api/v1/targets/1/')
    data = get_json(r)

    assert r.status_code == 404
    assert "id 1" in data['message']


def test_single_nonexistent(app, db):

    del db

    # fetch and verify
    r = app.test_client().get('/api/v1/targets/1/')
    data = get_json(r)

    assert r.status_code == 404
    assert "id 1" in data['message']
