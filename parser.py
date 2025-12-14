import re

def parse_sql(query: str) -> dict:
    """
    Parses a simple SQL query and returns a structured dict.
    Works perfectly with the corrected engine.py.
    """
    original_query = query
    query = query.strip()
    
    # Optional semicolon
    if query.endswith(';'):
        query = query[:-1].strip()

    # Must start with SELECT
    if not query.upper().startswith('SELECT '):
        raise ValueError("Query must start with SELECT")

    # Split into SELECT and FROM parts
    parts = re.split(r'\s+FROM\s+', query, flags=re.IGNORECASE)
    if len(parts) != 2:
        raise ValueError("Invalid query: missing or malformed FROM clause")

    select_part = parts[0][6:].strip()  # Remove 'SELECT'
    rest = parts[1].strip()

    # Split FROM and optional WHERE
    where_part = None
    if ' WHERE ' in rest.upper():
        from_part, where_part = re.split(r'\s+WHERE\s+', rest, flags=re.IGNORECASE)
    else:
        from_part = rest

    from_part = from_part.strip()
    if where_part:
        where_part = where_part.strip()

    # Parse table name - preserve original case
    table_match = re.match(r'^(\w+)', from_part)
    if not table_match:
        raise ValueError("Invalid table name")
    table = table_match.group(1)

    # Parse SELECT columns or COUNT
    select_cols = []
    select_upper = select_part.upper()

    if select_upper == '*':
        select_cols = ['*']
    elif select_upper.startswith('COUNT(') and select_upper.endswith(')'):
        count_arg = select_part[6:-1].strip()  # Remove COUNT( and )
        count_arg_upper = count_arg.upper()
        if count_arg_upper == '*' or re.match(r'^\w+$', count_arg_upper):
            select_cols = [f'COUNT({count_arg})']
        else:
            raise ValueError("Invalid argument in COUNT()")
    else:
        # List of columns: name, age, country
        cols = [col.strip() for col in select_part.split(',')]
        for col in cols:
            if not re.match(r'^\w+$', col):
                raise ValueError(f"Invalid column name: {col}")
        select_cols = cols  # Keep original case for output headers

    # Parse WHERE clause (single condition only)
    where = None
    if where_part:
        # Regex handles: column op value, with optional spaces
        match = re.match(
            r'^(\w+)\s*(=|!=|>=|<=|>|<)\s*(.+)$',
            where_part,
            re.IGNORECASE
        )
        if not match:
            raise ValueError(
                "Invalid WHERE clause. Expected: column operator value\n"
                "Examples: age > 30, country = 'USA', price <= 500"
            )

        raw_col, raw_op, val_str = match.groups()
        col = raw_col.upper()          # Normalize for engine lookup
        op = raw_op.upper()            # =, !=, >, <, >=, <=

        val_str = val_str.strip()

        # Parse value
        if val_str.startswith("'") and val_str.endswith("'"):
            val = val_str[1:-1]
            val_type = str
        else:
            # Try float first (to catch 999.99), then int
            try:
                if '.' in val_str:
                    val = float(val_str)
                else:
                    val = int(val_str)
                val_type = type(val)
            except ValueError:
                raise ValueError(f"Invalid numeric or quoted value: {val_str}")

        where = {
            'col': col,
            'op': op,
            'val': val,
            'type': val_type
        }

    return {
        'select': select_cols,
        'from': table,       # e.g., 'sample1'
        'where': where
    }