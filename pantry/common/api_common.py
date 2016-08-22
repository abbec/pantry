import json


def get_columns(parameters, columns):
    cols = []

    for col in parameters.get('fields', "").split(','):
        if col in columns:
            cols.append(columns[col])

    return cols if len(cols) > 0 else columns


def filter_columns(parameters, query, supported_columns):

    for c in supported_columns:
        if c.name in parameters:
            # try to parse json
            # this is to be able to support filtering like
            # url?parameter={"gt":45} for e.g. greater than
            value = parameters[c.name]
            try:
                j = json.loads(value)
                if "gt" in j:
                    query = query.where(c > j['gt'])
                elif "gte" in j:
                    query = query.where(c >= j['gte'])

                if "lt" in j:
                    query = query.where(c < j['lt'])
                elif "lte" in j:
                    query = query.where(c <= j['lte'])

            except ValueError:
                query = query.where(c == value)

    return query
