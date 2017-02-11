from pantry.db import db, migrate
import pantry.db.targets as tgttbl
import pantry.common.api_common as common


def init(app):
    db.init_app(app)
    migrate.init_app(app, db)


def clear():
    db.reflect()
    db.drop_all()


def get_target_columns(fields):

    if not fields:
        return [tgttbl.targets_table,
                tgttbl.tags_table.c.key,
                tgttbl.tags_table.c.value]

    filtered_cols = []
    if 'tags' in fields:
        filtered_cols.append(tgttbl.tags_table.c.key)
        filtered_cols.append(tgttbl.tags_table.c.value)

    if 'hostname' in fields:
        filtered_cols.append(tgttbl.targets_table.c.hostname)

    if 'nickname' in fields:
        filtered_cols.append(tgttbl.targets_table.c.nickname)

    if 'description' in fields:
        filtered_cols.append(tgttbl.targets_table.c.description)

    if 'maintainer' in fields:
        filtered_cols.append(tgttbl.targets_table.c.maintainer)

    if 'healthPercent' in fields:
        filtered_cols.append(tgttbl.targets_table.c.health_percent)

    if 'state' in fields:
        filtered_cols.append(tgttbl.targets_table.c.state)

    # always fetch id
    filtered_cols.append(tgttbl.targets_table.c.target_id)

    return filtered_cols


def db_targets_to_dict(db_targets):

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


def get_targets(params):

    fields = common.get_fields_from_params(params)
    columns = get_target_columns(fields)

    q = db.select(columns)
    q = q.select_from(db.join(
        tgttbl.targets_table,
        tgttbl.tags_table,
        isouter=True))

    # filter standard columns
    q = common.filter_columns(params, q,
                              [tgttbl.targets_table.c.hostname,
                               tgttbl.targets_table.c.nickname,
                               tgttbl.targets_table.c.health_percent])

    # filter tags
    for k, v in params.to_dict().items():
        if k not in common.reserved_params and k not in tgttbl.targets_table.c:
            q = q.where(tgttbl.tags_table.c.key == k)
            q = common.expr_to_query(q, tgttbl.tags_table.c.value, v)

    res = db.engine.execute(q).fetchall()
    return db_targets_to_dict(res)


def get_target(target_id, params=None):
    fields = common.get_fields_from_params(params)
    columns = get_target_columns(fields)

    q = db.select(columns)
    q = q.select_from(tgttbl.targets_table.outerjoin(tgttbl.tags_table))
    q = q.where(tgttbl.targets_table.c.target_id == target_id)

    result = db.engine.execute(q).fetchall()
    return next(iter(db_targets_to_dict(result)), None)


def create_target(content):

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
    q = tgttbl.targets_table.insert(db_target)
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
            db.engine.execute(tgttbl.tags_table.insert(), db_tags)

    return target_id


def delete_target(target_id):
    r = db.engine.execute(
        tgttbl.targets_table.delete().
        where(tgttbl.targets_table.c.target_id == target_id))

    return r.rowcount != 0
