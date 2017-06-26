import pantry.common.api_common as common
from pantry.db import db as db

# declare lease table
leases_table = db.Table(
    'leases',
    db.metadata,
    db.Column('lease_id', db.Integer, primary_key=True),
    db.Column('length', db.Integer),
    db.Column('timeout', db.Integer),
    db.Column('created_at', db.DateTime),
)

assignment_table = db.Table(
    'assigned_targets',
    db.Column(
        'lease_id',
        db.Integer,
        db.ForeignKey("leases.lease_id"),
        nullable=False),
    db.Column(
        'target_id',
        db.Integer,
        db.ForeignKey("targets.target_id"),
        nullable=False),
    db.Column('created_at', db.DateTime),
    db.Column('expires_at', db.DateTime),
)


def get_columns(fields):

    if not fields:
        return [leases_table]

    filtered_cols = []
    if 'length' in fields:
        filtered_cols.append(leases_table.c.length)

    if 'timeout' in fields:
        filtered_cols.append(leases_table.c.timeout)

    if 'created_at' in fields:
        filtered_cols.append(leases_table.c.created_at)

    filtered_cols.append(leases_table.c.lease_id)
    return filtered_cols


def to_dict(db_leases):
    leases = {}

    for l in db_leases:
        if l.lease_id not in leases:
            lease = leases[l.lease_id] = {"id": l.lease_id}

            if 'length' in l:
                lease['length'] = l.length

    return leases


def get(params):
    fields = common.get_fields_from_params(params)
    columns = get_columns(fields)

    q = db.select(columns)
    q = q.select_from(leases_table)

    # todo: add filters on state
    res = db.engine.execute(q).fetchall()
    return to_dict(res)
