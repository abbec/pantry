import json
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


def test_single(app, db):

    # insert an event
    tgt = fake.create_targets(1)
    db.engine.execute(targets_table.insert(), tgt)

    # fetch and verify
    r = app.test_client().get('/api/v1/targets/1/')
    data = get_json(r)

    assert r.status_code == 200
    assert data["hostname"] is not None


def test_single_nonexistent(app, db):

    del db

    # fetch and verify
    r = app.test_client().get('/api/v1/targets/1/')
    data = get_json(r)

    assert r.status_code == 404
    assert "id 1" in data['message']
