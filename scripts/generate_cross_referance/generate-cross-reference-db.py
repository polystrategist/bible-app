import os
import re
import sqlite3

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
GENERATED_DIR = os.path.join(SCRIPT_DIR, "generated")
DB_PATH = os.path.join(GENERATED_DIR, "cross_references.db")

# ---------------------------------------------------------------------------
# MySQL → SQLite transformations
# ---------------------------------------------------------------------------

def mysql_to_sqlite_create(statement: str) -> list[str]:
    """
    Convert a MySQL CREATE TABLE statement to SQLite-compatible DDL.
    Returns the CREATE TABLE string plus any CREATE INDEX strings needed.
    """
    # Collect index columns from inline INDEX directives
    index_cols = re.findall(r"INDEX\s*\(`?(\w+)`?\)", statement, re.IGNORECASE)

    # Remove inline INDEX lines
    statement = re.sub(r"\s*,?\s*INDEX\s*\([^)]+\)", "", statement)

    # Fix trailing comma before closing paren that removal may leave
    statement = re.sub(r",\s*(\n\s*\))", r"\1", statement)

    # MySQL: INT AUTO_INCREMENT PRIMARY KEY → SQLite: INTEGER PRIMARY KEY AUTOINCREMENT
    statement = re.sub(
        r"\bINT\s+AUTO_INCREMENT\s+PRIMARY\s+KEY\b",
        "INTEGER PRIMARY KEY AUTOINCREMENT",
        statement,
        flags=re.IGNORECASE,
    )

    # Strip backtick quoting (SQLite supports it, but keep it clean)
    statement = statement.replace("`", "")

    # Extract table name for index creation
    table_match = re.search(r"CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?(\w+)", statement, re.IGNORECASE)
    table_name = table_match.group(1) if table_match else "unknown"

    statements = [statement.strip()]
    for col in index_cols:
        statements.append(
            f"CREATE INDEX IF NOT EXISTS idx_{table_name}_{col} ON {table_name} ({col})"
        )

    return statements


def mysql_to_sqlite_insert(statement: str) -> str:
    return statement.replace("`", "").strip()


def strip_leading_comments(stmt: str) -> str:
    """Remove leading blank lines and -- comment lines from a statement."""
    lines = stmt.split("\n")
    for i, line in enumerate(lines):
        if line.strip() and not line.strip().startswith("--"):
            return "\n".join(lines[i:]).strip()
    return ""


def split_statements(sql: str) -> list[str]:
    """Split SQL text into individual statements on semicolons."""
    raw = [strip_leading_comments(s) for s in sql.split(";")]
    return [s for s in raw if s]


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

os.makedirs(GENERATED_DIR, exist_ok=True)

if os.path.exists(DB_PATH):
    os.remove(DB_PATH)
    print(f"Removed existing DB: {DB_PATH}")

sql_files = sorted(
    f for f in os.listdir(GENERATED_DIR) if f.endswith(".sql")
)

if not sql_files:
    print("No .sql files found in generated/. Run update-sql-using-our-book.py first.")
    raise SystemExit(1)

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()
cursor.execute("PRAGMA journal_mode=WAL")
cursor.execute("PRAGMA synchronous=NORMAL")

total_rows = 0

for filename in sql_files:
    path = os.path.join(GENERATED_DIR, filename)
    print(f"Processing {filename} …")

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    statements = split_statements(content)
    file_rows = 0

    for stmt in statements:
        upper = stmt.upper().lstrip()

        try:
            if upper.startswith("CREATE TABLE"):
                for ddl in mysql_to_sqlite_create(stmt):
                    cursor.execute(ddl)

            elif upper.startswith("INSERT"):
                cursor.execute(mysql_to_sqlite_insert(stmt))
                file_rows += 1

            # Skip anything else (comments, empty, unknown)

        except sqlite3.Error as e:
            print(f"\nSQL ERROR in {filename}: {e}")
            print(f"  Statement preview: {stmt[:200]!r}")
            conn.close()
            raise SystemExit(1)

    conn.commit()
    total_rows += file_rows
    print(f"  Inserted {file_rows:,} rows")

conn.close()
print(f"\nDone. Total rows: {total_rows:,}")
print(f"Database: {DB_PATH}")
