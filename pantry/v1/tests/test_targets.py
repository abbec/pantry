import json
import pantry.fake as fake


def get_json(response):
    return json.loads(response.get_data(as_text=True))


def test_list(app, backend):

    # insert an event
    tgt = fake.create_targets(1)
    backend.create_target(tgt[0])

    # fetch and verify
    r = app.test_client().get('/api/v1/targets/')
    data = get_json(r)

    assert data['targets']


def test_list_fields(app, backend):

    # insert an event
    tgt = fake.create_targets(1)
    backend.create_target(tgt[0])

    # fetch and verify
    r = app.test_client().get('/api/v1/targets/?fields=hostname')
    data = get_json(r)

    assert data['targets']
    assert data['targets'][0]['hostname'] == tgt[0]['hostname']
    assert 'nickname' not in data['targets'][0]


def test_list_filter(app, backend):

    # insert an event
    tgt = fake.create_targets(2)
    tgt[0]['hostname'] = "sune"
    tgt[1]['hostname'] = "suna"
    backend.create_target(tgt[0])
    backend.create_target(tgt[1])

    # fetch and verify
    r = app.test_client().get('/api/v1/targets/?hostname=sune')
    data = get_json(r)

    assert len(data['targets']) == 1
    assert data['targets'][0]['hostname'] == "sune"


def test_single(app, backend):

    # insert an event
    tgt = fake.create_targets(1)
    backend.create_target(tgt[0])

    # fetch and verify
    r = app.test_client().get('/api/v1/targets/1/')
    data = get_json(r)

    assert r.status_code == 200
    assert data["hostname"] is not None


def test_create(app, backend):

    del backend

    target = {
        "hostname": "sune",
        "description": "Awesome host",
        "maintainer": "sune@suneco.biz",
        "tags": [
            {"key": "platform", "value": "linux"},
            {"key": "gpu", "value": "amd"}]
        }

    r = app.test_client().post('/api/v1/targets/', data=json.dumps(target))

    data = get_json(r)
    assert r.status_code == 201
    assert "id" in data
    assert 'Location' in r.headers

    assert data['hostname'] == target['hostname']

    assert len(data['tags']) == 2


def test_delete(app, backend):

    # insert an event
    tgt = fake.create_targets(1)
    backend.create_target(tgt[0])

    # fetch and verify
    r = app.test_client().delete('/api/v1/targets/1/')

    assert r.status_code == 204


def test_delete_nonexistent(app, backend):

    del backend

    # fetch and verify
    r = app.test_client().delete('/api/v1/targets/1/')
    assert r.status_code == 404

    data = get_json(r)
    assert "id 1" in data['message']


def test_single_nonexistent(app, backend):

    del backend

    # fetch and verify
    r = app.test_client().get('/api/v1/targets/1/')
    data = get_json(r)

    assert r.status_code == 404
    assert "id 1" in data['message']
