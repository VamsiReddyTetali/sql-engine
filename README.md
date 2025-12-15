# Mini In-Memory SQL Query Engine

This is a small Python project I built to better understand what happens inside a database when you run a simple SQL query. It loads CSV files into memory and lets you run basic SELECT queries with filtering (WHERE) and counting (COUNT) — all from the command line.

## Features

-   Loads any CSV file(s). The table name is just the filename without `.csv`.
-   **Supported SQL Grammar:**
    -   `SELECT * FROM table`
    -   `SELECT column1, column2 FROM table`
    -   `SELECT * FROM table WHERE column op value` (operators: **=, !=, >, <, >=, <=**)
    -   String values must be in single quotes: `country = 'USA'`
    -   `SELECT COUNT(*) FROM table`
    -   `SELECT COUNT(column) FROM table`
-   **Limitations:** Only one WHERE condition (no AND/OR yet) and no support for JOINs, GROUP BY, or ORDER BY.
-   Runs as an interactive prompt (REPL) with friendly error messages.

## How to Run

1.  Make sure you have Python 3 installed.
2.  Open a terminal in the project folder.
3.  Run the CLI, pointing it to your CSV files:
    ```bash
    python cli.py data/sample1.csv data/sample2.csv
    ```

You’ll see the tables load, then a `>` prompt appears. Type your query and press Enter.

**Examples:**
```text
> SELECT name, age FROM sample1 WHERE age > 30
name    age
Charlie 35
David   40

> SELECT COUNT(*) FROM sample2 WHERE price < 600
COUNT
2

> SELECT * FROM sample1 WHERE country = 'Canada'
name    age     country id
Bob     30      Canada  2
Type exit or quit to stop.

Project Files
parser.py – I wrote my own parser using regex and string splitting. I avoided libraries because I wanted to really learn how query parsing works from scratch—it was challenging but totally worth it.

engine.py – This is the core execution logic: it loads the CSV, stores rows as a list of dictionaries, applies the WHERE filter, handles COUNT, and performs the final projection (selecting columns).

cli.py – Simple loop that reads your queries, runs them against the engine, and prints results in a clean, readable table format.

data/ – Contains two small CSV files I created myself (sample1.csv for people data, sample2.csv for products) since no dataset was provided with the task.

What Was Hard and What I Learned
The parser was definitely the toughest part. Things like making sure it could handle operators like age>=30 (no space) and handling case sensitivity between query text and the actual column headers kept breaking it. I spent a lot of time fixing regex patterns and normalizing column names to uppercase internally while keeping the output column names looking nice for the user.

I also realized how convenient a list of dictionaries is for this kind of project—filtering and selecting columns felt very natural—but it instantly shows why real databases use more optimized, columnar structures for huge datasets. This whole thing made SQL feel way less like magic.