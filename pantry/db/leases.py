from pantry.db import db as database

# declare lease table
leases_table = database.Table(
    'leases',
    database.metadata,
    database.Column('lease_id', database.Integer, primary_key=True),
)

assignment_table = database.Table(
    'assigned_targets',
    database.Column('lease_id', database.Integer,
                    database.ForeignKey("leases.lease_id"),
                    nullable=False),
    database.Column('target_id', database.Integer,
                    database.ForeignKey("targets.target_id"),
                    nullable=False)
)
