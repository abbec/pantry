import json

reserved_params = ["limit", "fields", "offset"]


def get_fields_from_params(params):

    if not params:
        return []

    fields = params.get('fields', "")
    fields = fields.split(",")


def filter_columns(params, query, supported_columns):

    for c in supported_columns:
        if c.name in params:
            query = expr_to_query(query, c, params[c.name])

    return query


def expr_to_query(q, col, expression):
    # try to parse json
    # this is to be able to support filtering like
    # url?parameter={"gt":45} for e.g. greater than
    try:
        j = json.loads(expression)
        if "gt" in j:
            q = q.where(col > j['gt'])
        elif "gte" in j:
            q = q.where(col >= j['gte'])

        if "lt" in j:
            q = q.where(col < j['lt'])
        elif "lte" in j:
            q = q.where(col <= j['lte'])

    except ValueError:
        q = q.where(col == expression)

    return q
