import sqlite3
from datetime import datetime

DB_PATH = "bioinsight.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            file_type TEXT,
            report_text TEXT,
            created_at TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_report(filename, file_type, report_text):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO reports (filename, file_type, report_text, created_at) VALUES (?, ?, ?, ?)",
        (filename, file_type, report_text, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()

def get_all_reports():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, filename, file_type, created_at FROM reports ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return [
        {"id": r[0], "filename": r[1], "file_type": r[2], "created_at": r[3]}
        for r in rows
    ]

def get_report_by_id(report_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT report_text FROM reports WHERE id = ?", (report_id,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None

if __name__ == "__main__":
    init_db()
    save_report("test.csv", "tabular", "This is a test report.")
    print(get_all_reports())
    