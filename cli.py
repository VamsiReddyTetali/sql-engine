# cli.py
from parser import parse_sql
from engine import Database
import sys

def print_results(results: list):
    if not results:
        print("No results")
        return
    
    # Get headers (use the keys from first row)
    headers = list(results[0].keys())
    # Print header
    print("\t".join(headers))
    # Print rows
    for row in results:
        print("\t".join(str(row.get(h, '')) for h in headers))

def main():
    if len(sys.argv) < 2:
        print("Usage: python cli.py path/to/csv1.csv [path/to/csv2.csv ...]")
        sys.exit(1)
    
    db = Database()
    for csv_path in sys.argv[1:]:
        try:
            db.load_table(csv_path)
        except Exception as e:
            print(f"Error loading {csv_path}: {e}")
            sys.exit(1)
    
    print("=== Mini SQL Engine REPL ===")
    print("Type your SQL query (end with ; optional). Type 'exit' or 'quit' to quit.\n")
    
    while True:
        try:
            query = input("> ").strip()
            if query.lower() in ['exit', 'quit', 'q']:
                print("Goodbye!")
                break
            if not query:
                continue
                
            parsed = parse_sql(query)
            results = db.execute_query(parsed)
            print_results(results)
            print()  # Blank line for readability
        except ValueError as ve:
            print(f"SQL Error: {ve}")
        except Exception as e:
            print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()