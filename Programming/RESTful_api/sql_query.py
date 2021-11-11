def gen_search(table, fields, sort_by='', sort_type='desc', s=''):
    sql = f"SELECT * FROM {table}"
    if s:
        sql += ' WHERE ' + f" LIKE '%{s}%' OR ".join(fields) + f" LIKE '%{s}%'"
    if sort_by:
        if sort_type.lower() not in ['asc', 'desc']:
            sort_type = 'desc'
        sql += f" ORDER BY {sort_by} {sort_type}"
    return sql


def gen_search_by_field(table, field, val):
    return f"SELECT * FROM {table} WHERE {field}='{val}'"
