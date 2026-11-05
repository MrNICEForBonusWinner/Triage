import sqlite3

DB = "triage.db"


def _run(sql, args=()):
    with sqlite3.connect(DB) as db:
        db.row_factory = sqlite3.Row
        db.execute("CREATE TABLE IF NOT EXISTS issues (id INTEGER PRIMARY KEY, title TEXT NOT NULL, status TEXT NOT NULL)")
        cur = db.execute(sql, args)
        return cur.lastrowid, [dict(r) for r in cur.fetchall()]


def list_issues():
    return _run("SELECT * FROM issues")[1]


def get_issue(issue_id):
    rows = _run("SELECT * FROM issues WHERE id = ?", (issue_id,))[1]
    return rows[0] if rows else None


def insert_issue(title):
    new_id = _run("INSERT INTO issues (title, status) VALUES (?, 'open')", (title,))[0]
    return get_issue(new_id)


def update_status(issue_id, status):
    _run("UPDATE issues SET status = ? WHERE id = ?", (status, issue_id))
    return get_issue(issue_id)


def delete_issue(issue_id):
    _run("DELETE FROM issues WHERE id = ?", (issue_id,))
