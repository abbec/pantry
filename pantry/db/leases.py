from pantry.db import db as database

# declare lease table
leases_table = database.Table(
    'leases',
    database.metadata,
    database.Column('lease_id', database.Integer, primary_key=True),
    database.Column('state', database.Enum(
        "assigningtargets", "ended", "active")),
    database.Column('fulfilled', database.Boolean),
    database.Column('time', database.Integer),
    database.Column('created_at', database.DateTime),
    database.Column('updated_at', database.DateTime)
)

assignment_table = database.Table(
    'assigned_targets',
    database.Column('lease_id', database.Integer,
                    database.ForeignKey("leases.lease_id"),
                    nullable=False),
    database.Column('target_id', database.Integer,
                    database.ForeignKey("targets.target_id"),
                    nullable=False),
    database.Column('created_at', database.DateTime),
)
