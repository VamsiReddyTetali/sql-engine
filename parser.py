import re

def parse_sql(query: str) -> dict:
    # Normalize query
    original_query = query
    query = query.strip().upper()
    if not query.endswith(';'):
        query += ';'
    
    if not query.startswith('SELECT '):
        raise ValueError("Query must start with SELECT")
    
    # Split into SELECT and FROM parts
    parts = query.split(' FROM ')
    if len(parts) != 2:
        raise ValueError("Invalid query format. Expected SELECT ... FROM ...")
    
    select_part = parts[0][7:].strip()  # After SELECT
    from_where_part = parts[1].rstrip(';').strip()
    
    # Split FROM and WHERE
    from_where = from_where_part.split(' WHERE ')
    from_part = from_where[0].strip()
    where_part = None
    if len(from_where) == 2:
        where_part = from_where[1].strip()
    elif len(from_where) > 2:
        raise ValueError("Invalid WHERE clause")
    
    # Parse SELECT
    select_cols = []
    if select_part == '*':
        select_cols = ['*']
    elif select_part.startswith('COUNT(') and select_part.endswith(')'):
        count_arg = select_part[6:-1].strip()
        if count_arg == '*' or re.match(r'^\w+$', count_arg):
            select_cols = [f'COUNT({count_arg})']
        else:
            raise ValueError("Invalid COUNT argument")
    else:
        select_cols = [c.strip() for c in select_part.split(',')]
        if not all(re.match(r'^\w+$', c) for c in select_cols):
            raise ValueError("Invalid column names in SELECT")
    
    # Parse FROM (table name)
    table = from_part
    if not re.match(r'^\w+$', table):
        raise ValueError("Invalid table name")
    
    # Parse WHERE (single condition)
    where = None
    if where_part:
        # Match col op val
        match = re.match(r'^(\w+)\s*(=|\!=|>|<\s*|>=|<=)\s*(.+)$', where_part)
        if not match:
            raise ValueError("Invalid WHERE clause. Expected: column op value")
        col, op, val_str = match.groups()
        # Normalize op
        op = op.strip()
        # Parse value
        if val_str.startswith("'") and val_str.endswith("'"):
            val = val_str[1:-1]
            val_type = str
        else:
            try:
                val = int(val_str)
                val_type = int
            except ValueError:
                try:
                    val = float(val_str)
                    val_type = float
                except ValueError:
                    raise ValueError(f"Invalid value in WHERE: {val_str}")
        where = {'col': col, 'op': op, 'val': val, 'type': val_type}
    
    return {
        'select': select_cols,
        'from': table,
        'where': where
    }