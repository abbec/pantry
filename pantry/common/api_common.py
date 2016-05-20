
def get_columns(parameters, columns):
    cols = []

    for col in parameters.get('fields', "").split(','):
        if col in columns:
            cols.append(columns[col])

    return cols if len(cols) > 0 else columns
