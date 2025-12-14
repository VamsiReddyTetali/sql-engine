\# Simplified In-Memory SQL Query Engine



\## Overview

This is a basic Python-based SQL engine that loads data from CSV files into memory and executes simple SQL queries. It supports projection (SELECT), filtering (WHERE with single condition), and aggregation (COUNT).



\## Setup and Run

1\. Clone the repository: `git clone https://github.com/VamsiReddyTetali/sql-engine.git`

2\. Navigate to the directory: `cd sql-engine`

3\. Run the CLI: `python cli.py data/sample1.csv data/sample2.csv` (you can load multiple CSVs)

4\. In the REPL prompt (>), enter SQL queries. Type 'exit' or 'quit' to quit.



\## Supported SQL Grammar

The engine supports a subset of SQL:

\- `SELECT \* FROM table;` (select all columns)

\- `SELECT col1, col2 FROM table;` (select specific columns)

\- `SELECT \* FROM table WHERE col op value;` (filter with =, !=, >, <, >=, <=; value as number or 'string')

\- `SELECT COUNT(\*) FROM table;` (count rows)

\- `SELECT COUNT(col) FROM table;` (count non-null in column)

\- Optional semicolon (;).

\- Single WHERE condition only.

\- Table name is derived from CSV filename (e.g., 'sample1' for 'sample1.csv').



Examples:

\- `SELECT name, age FROM sample1 WHERE age > 30;`

\- `SELECT COUNT(\*) FROM sample2 WHERE price < 500;`



Limitations: No JOINs, GROUP BY, multiple WHERE conditions, or advanced features.



\## Testing

Tested with `data/sample1.csv` (people data) and `data/sample2.csv` (products data). The code handles errors like invalid syntax, non-existent columns, and type mismatches gracefully.

