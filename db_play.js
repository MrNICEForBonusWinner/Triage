import Database from "better-sqlite3";

const db = new Database("triage.db");

db.exec(`CREATE TABLE IF NOT EXISTS issues (
  id INTEGER PRIMARY KEY,
  title TEXT NOT NULL,
  status TEXT NOT NULL
)`);

const { n } = db.prepare("SELECT COUNT(*) AS n FROM issues").get();
if (n === 0) {
  const insert = db.prepare("INSERT INTO issues (title, status) VALUES (?, ?)");
  insert.run("Login button does nothing on mobile", "open");
  insert.run("Export report as CSV", "open");
}

console.log("All issues:", db.prepare("SELECT * FROM issues").all());

db.prepare("UPDATE issues SET status = 'done' WHERE id = ?").run(2);

console.log("Done issues:", db.prepare("SELECT * FROM issues WHERE status = 'done'").all());