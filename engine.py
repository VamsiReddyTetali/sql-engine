import csv
import os

class Database:
    def __init__(self):
        self.tables = {}  # {'table_name': [list of dict rows]}

    def load_table(self, csv_path: str):
        """
        Loads a CSV file into memory.
        Table name = filename without extension (e.g., sample1.csv → 'sample1')
        Column names are converted to UPPERCASE for case-insensitive querying.
        """
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"CSV file not found: {csv_path}")

        table_name = os.path.basename(csv_path).rsplit('.', 1)[0]  # Remove extension
        if table_name in self.tables:
            print(f"Table '{table_name}' already loaded.")
            return

        rows = []
        with open(csv_path, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row_dict in reader:
                # Normalize: strip whitespace, convert types, uppercase keys
                normalized_row = {}
                for key, value in row_dict.items():
                    stripped = value.strip() if value is not None else ''
                    if stripped == '':
                        normalized_row[key.upper()] = None
                    else:
                        try:
                            normalized_row[key.upper()] = int(stripped)
                        except ValueError:
                            try:
                                normalized_row[key.upper()] = float(stripped)
                            except ValueError:
                                normalized_row[key.upper()] = stripped
                rows.append(normalized_row)

        self.tables[table_name] = rows
        print(f"Loaded table '{table_name}' with {len(rows)} rows from {csv_path}")

    def execute_query(self, parsed_query: dict):
        """
        Executes the parsed query and returns list of dicts (or [{'COUNT': n}] for aggregates)
        """
        table_name = parsed_query['from']
        if table_name not in self.tables:
            raise ValueError(f"Table '{table_name}' not loaded. Available: {list(self.tables.keys())}")

        rows = self.tables[table_name][:]  # Copy to avoid modifying original

        # Apply WHERE filter
        where = parsed_query['where']
        if where:
            col = where['col'].upper()
            op = where['op']
            val = where['val']
            val_type = where['type']

            if col not in rows[0]:
                raise ValueError(f"Column '{where['col']}' does not exist in table '{table_name}'")

            filtered = []
            for row in rows:
                row_val = row.get(col)

                # Skip if None and not comparable
                if row_val is None:
                    continue

                # Coerce row value to expected type if possible
                try:
                    row_val = val_type(row_val)
                except (ValueError, TypeError):
                    continue  # Type mismatch → skip row

                # Perform comparison
                match = False
                if op == '=':
                    match = row_val == val
                elif op == '!=':
                    match = row_val != val
                elif op == '>':
                    match = row_val > val
                elif op == '<':
                    match = row_val < val
                elif op == '>=':
                    match = row_val >= val
                elif op == '<=':
                    match = row_val <= val

                if match:
                    filtered.append(row)

            rows = filtered

        # Handle SELECT
        select = parsed_query['select']

        # Aggregation: COUNT
        if len(select) == 1 and select[0].startswith('COUNT('):
            count_arg = select[0][6:-1].strip()  # '*' or 'COLUMN'
            if count_arg == '*':
                count = len(rows)
            else:
                count_col = count_arg.upper()
                if count_col not in rows[0]:
                    raise ValueError(f"Column '{count_arg}' does not exist for COUNT")
                count = sum(1 for row in rows if row.get(count_col) is not None)
            return [{'COUNT': count}]

        # Projection: SELECT * or specific columns
        if select == ['*']:
            return rows
        else:
            # Normalize selected columns to uppercase
            projected_cols = [col.upper() for col in select]
            projected = []
            for row in rows:
                new_row = {}
                for col in projected_cols:
                    if col not in row:
                        raise ValueError(f"Column '{select[projected_cols.index(col)]}' does not exist")
                    new_row[select[projected_cols.index(col)]] = row[col]  # Keep original case in output
                projected.append(new_row)
            return projected