from pantry.db import db as database
# import enum

# todo: this is not supported in SQLAlchemy until version 1.1
# class TargetStates(enum.Enum):
#    ready = "Ready"
#    leased = "Leased"
#    down = "Down"
#    maintenance = "Down for maintenance"

# declare targets table
targets_table = database.Table(
    'targets',
    database.metadata,
    database.Column('target_id', database.Integer, primary_key=True),
    database.Column('hostname', database.String(60), nullable=False),
    database.Column('nickname', database.String(60)),
    database.Column('description', database.String(60), nullable=False),
    database.Column('maintainer', database.String(60), nullable=False),
    database.Column('health_percent', database.Integer),
    database.Column('state', database.Enum(
        "ready", "leased", "down", "maintenance"))
    )
