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


def test_single(app, db):

    # insert an event
    tgt = fake.create_targets(1)
    db.engine.execute(targets_table.insert(), tgt)

    # fetch and verify
    r = app.test_client().get('/api/v1/targets/1/')
    data = get_json(r)

    assert r.status_code == 200
    assert data["hostname"] is not None
