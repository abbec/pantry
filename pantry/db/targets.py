from pantry.db import db as db
import pantry.common.api_common as common
# import enum

# todo: this is not supported in SQLAlchemy until version 1.1
# class TargetStates(enum.Enum):
#    ready = "Ready"
#    leased = "Leased"
#    down = "Down"
#    maintenance = "Down for maintenance"

# declare targets table
targets_table = db.Table(
    'targets',
    db.metadata,
    db.Column('target_id', db.Integer, primary_key=True),
    db.Column('hostname', db.String(60), nullable=False),
    db.Column('nickname', db.String(60)),
    db.Column('description', db.String(60), nullable=False),
    db.Column('maintainer', db.String(60), nullable=False),
    db.Column('health_percent', db.Integer, nullable=False, default=100),
    db.Column('state', db.Enum(
        "ready", "leased", "down", "maintenance"))
)

tags_table = db.Table(
    'target_tags',
    db.metadata,
    db.Column('tag_id', db.Integer, primary_key=True),
    db.Column('key', db.String(64), nullable=False),
    db.Column('value', db.String(256), nullable=False),
    db.Column('target_id',
              db.Integer,
              db.ForeignKey("targets.target_id"),
              nullable=False)
)


def get_columns(fields):

    if not fields:
        return [targets_table,
                tags_table.c.key,
                tags_table.c.value]

    filtered_cols = []
    if 'tags' in fields:
        filtered_cols.append(tags_table.c.key)
        filtered_cols.append(tags_table.c.value)

    if 'hostname' in fields:
        filtered_cols.append(targets_table.c.hostname)

    if 'nickname' in fields:
        filtered_cols.append(targets_table.c.nickname)

    if 'description' in fields:
        filtered_cols.append(targets_table.c.description)

    if 'maintainer' in fields:
        filtered_cols.append(targets_table.c.maintainer)

    if 'healthPercent' in fields:
        filtered_cols.append(targets_table.c.health_percent)

    if 'state' in fields:
        filtered_cols.append(targets_table.c.state)

    # always fetch id
    filtered_cols.append(targets_table.c.target_id)

    return filtered_cols


def to_dict(db_targets):

    targets = {}

    for t in db_targets:
        if t.target_id not in targets:
            target = targets[t.target_id] = {"id": t.target_id}

            if 'hostname' in t:
                target['hostname'] = t.hostname

            if 'description' in t:
                target['description'] = t.description

            if 'maintainer' in t:
                target['maintainer'] = t.maintainer

            if 'health_percent' in t:
                target['healthPercent'] = t.health_percent

            if 'state' in t:
                target['state'] = t.state

            if "key" in t and "value" in t:
                target['tags'] = []

        if "key" in t and "value" in t and t.key is not None:
            target['tags'].append(
                {"key": t.key, "value": t.value})

    return list(targets.values())


def get(params):
    fields = common.get_fields_from_params(params)
    columns = get_columns(fields)

    q = db.select(columns)
    q = q.select_from(db.join(
        targets_table,
        tags_table,
        isouter=True))

    # filter standard columns
    q = common.filter_columns(params, q,
                              [targets_table.c.hostname,
                               targets_table.c.nickname,
                               targets_table.c.health_percent])

    # filter tags
    for k, v in params.to_dict().items():
        if k not in common.reserved_params and k not in targets_table.c:
            q = q.where(tags_table.c.key == k)
            q = common.expr_to_query(q, tags_table.c.value, v)

    res = db.engine.execute(q).fetchall()
    return to_dict(res)


def get_single(target_id, params=None):
    fields = common.get_fields_from_params(params)
    columns = get_columns(fields)

    q = db.select(columns)
    q = q.select_from(targets_table.outerjoin(tags_table))
    q = q.where(targets_table.c.target_id == target_id)

    result = db.engine.execute(q).fetchall()
    return next(iter(to_dict(result)), None)


def create(content):
    # create database row, parsing explicitly to not
    # rely on names in sent in data
    db_target = {
        "hostname": content['hostname'],
        "description": content['description'],
        "maintainer": content['maintainer'],
    }

    if 'nickname' in content:
        db_target['nickname'] = content['nickname']

    if 'healthPercent' in content:
        db_target['health_percent'] = content['healthPercent']

    if 'state' in content:
        db_target['state'] = content['state']

    # insert targets
    q = targets_table.insert(db_target)
    result = db.engine.execute(q)
    target_id = result.inserted_primary_key[0]

    # insert tags for each target
    if 'tags' in content:
        db_tags = []
        for tag in content['tags']:
            db_tag = {
                "key": tag['key'],
                "value": tag['value'],
                "target_id": target_id
            }
            db_tags.append(db_tag)

        if db_tags:
            db.engine.execute(tags_table.insert(), db_tags)

    return target_id


def delete(target_id):

    r = db.engine.execute(
        targets_table.delete().
        where(targets_table.c.target_id == target_id))

    return r.rowcount != 0
