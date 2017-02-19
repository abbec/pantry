from pantry.db import db, migrate
import pantry.db.targets as targets


def init(app):
    db.init_app(app)
    migrate.init_app(app, db)


def clear():
    db.reflect()
    db.drop_all()


def get_targets(params):
    return targets.get(params)


def get_target(target_id, params=None):
    return targets.get_single(target_id, params)


def create_target(content):
    return targets.create(content)


def delete_target(target_id):
    return targets.delete(target_id)
