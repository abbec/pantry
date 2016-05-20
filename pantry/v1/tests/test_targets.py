import json, pytest
import pantry.db.fake as fake
from pantry.db.targets import targets_table

import json

def get_json(response):
    return json.loads(response.get_data(as_text=True))

class TestTargets(object):

    def test_list(self, app, db):

        # insert an event
        tgt = fake.create_targets(1)
        db.engine.execute(targets_table.insert().values(tgt))

        # fetch and verify
        r = app.test_client().get('/api/v1/targets/')
        data = get_json(r)

        assert len(data['targets']) > 0
