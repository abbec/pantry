import json
# import pantry.db.fake as fake


def get_json(response):
    return json.loads(response.get_data(as_text=True))


def test_list(app, backend):
    del app
    del backend

    # insert a lease
    # lease = fake.create_leases(1)
    # db.engine.execute(leases_table.insert(), lease)

    # # fetch and verify
    # r = app.test_client().get('/api/v1/leases/')
    # data = get_json(r)

    # assert len(data['leases']) > 0
