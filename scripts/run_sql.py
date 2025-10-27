import sys, duckdb, os, re

def main():
    if len(sys.argv) != 3:
        print("Usage: python run_sql.py <db_path> <sql_file>")
        sys.exit(1)

    db_path, sql_file = sys.argv[1], sys.argv[2]

    if not os.path.exists(db_path):
        print(f"❌ DuckDB file not found: {db_path}")
        sys.exit(1)
    if not os.path.exists(sql_file):
        print(f"❌ SQL file not found: {sql_file}")
        sys.exit(1)

    con = duckdb.connect(db_path)
    print(f"✅ Connected to: {db_path}")

    with open(sql_file, "r", encoding="utf-8") as f:
        script = f.read()

    # Remove BOM if present and normalize line endings
    script = script.replace("\r\n", "\n").replace("\r", "\n")

    # Split on semicolons NOT inside quotes (simple heuristic)
    # This covers most analytics scripts without complex procedures.
    parts = []
    buff = []
    in_single = in_double = False

    for ch in script:
        if ch == "'" and not in_double:
            in_single = not in_single
        elif ch == '"' and not in_single:
            in_double = not in_double
        if ch == ';' and not in_single and not in_double:
            parts.append(''.join(buff).strip())
            buff = []
        else:
            buff.append(ch)
    tail = ''.join(buff).strip()
    if tail:
        parts.append(tail)

    stmt_no = 0
    for stmt in parts:
        # skip empty and pure comments
        if not stmt or re.fullmatch(r"\s*(--.*\n?)*", stmt, flags=re.DOTALL):
            continue
        stmt_no += 1
        try:
            rel = con.execute(stmt)
            # If it likely returns rows, print a small preview
            if re.match(r"^\s*(WITH|SELECT|SHOW|PRAGMA|DESCRIBE)\b", stmt, re.IGNORECASE):
                df = rel.fetchdf()
                print(f"\n--- Result #{stmt_no} (rows={len(df)}) ---")
                # show up to 50 rows to keep output readable
                print(df.head(50))
            else:
                print(f"\n--- Statement #{stmt_no} OK ---")
        except Exception as e:
            print(f"\n*** Statement #{stmt_no} FAILED ***")
            print(e)
            print("SQL:\n" + stmt + "\n")

if __name__ == "__main__":
    main()
