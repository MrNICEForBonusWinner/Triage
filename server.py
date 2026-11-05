import sqlite3
from typing import Optional
from fastapi import FastAPI, HTTPException, Response
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, ConfigDict
from starlette.exceptions import HTTPException as StarletteHTTPException

app, DB = FastAPI(), "triage.db"


class NewIssue(BaseModel):
       model_config = ConfigDict(str_strip_whitespace=True, strict=True)
       title: str = Field(min_length=1, max_length=200)


class StatusUpdate(BaseModel):
    model_config = ConfigDict(strict=True)
    status: str



@app.exception_handler(RequestValidationError)
async def bad_request(request, exc):
    return JSONResponse({"error": exc.errors()[0]["msg"]}, status_code=400)


@app.exception_handler(StarletteHTTPException)
async def http_error(request, exc):
    return JSONResponse({"error": exc.detail}, status_code=exc.status_code)


def q(sql, args=()):
    with sqlite3.connect(DB) as db:
        db.row_factory = sqlite3.Row
        db.execute("CREATE TABLE IF NOT EXISTS issues (id INTEGER PRIMARY KEY, title TEXT NOT NULL, status TEXT NOT NULL)")
        cur = db.execute(sql, args)
        return cur.lastrowid, [dict(r) for r in cur.fetchall()]


@app.get("/api/issues")
@app.get("/api/issues/{i}")
def get_issues(i: Optional[int] = None):
    if not i:
        return q("SELECT * FROM issues")[1]
    rows = q("SELECT * FROM issues WHERE id = ?", (i,))[1]
    if not rows:
        raise HTTPException(404, "no such issue")
    return rows[0]


@app.post("/api/issues", status_code=201)
def add_issue(issue: NewIssue):
    new_id = q("INSERT INTO issues (title, status) VALUES (?, 'open')", (issue.title,))[0]
    return q("SELECT * FROM issues WHERE id = ?", (new_id,))[1][0]

@app.patch("/api/issues/{issue_id}/status")
def set_status(issue_id: int, body: StatusUpdate):
    if body.status not in ("open", "done"):
        raise HTTPException(400, "status must be 'open' or 'done'")
    if not q("SELECT id FROM issues WHERE id = ?", (issue_id,))[1]:
        raise HTTPException(404, "no such issue")
    q("UPDATE issues SET status = ? WHERE id = ?", (body.status, issue_id))
    return q("SELECT * FROM issues WHERE id = ?", (issue_id,))[1][0]


@app.delete("/api/issues/{issue_id}", status_code=204)
def delete_issue(issue_id: int):
    if not q("SELECT id FROM issues WHERE id = ?", (issue_id,))[1]:
        raise HTTPException(404, "no such issue")
    q("DELETE FROM issues WHERE id = ?", (issue_id,))
    return Response(status_code=204)
