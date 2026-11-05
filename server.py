from typing import Optional
from fastapi import FastAPI, HTTPException, Response
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, ConfigDict
from starlette.exceptions import HTTPException as StarletteHTTPException

import db

app = FastAPI()


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


@app.get("/api/issues")
@app.get("/api/issues/{i}")
def get_issues(i: Optional[int] = None):
    if not i:
        return db.list_issues()
    row = db.get_issue(i)
    if row is None:
        raise HTTPException(404, "no such issue")
    return row


@app.post("/api/issues", status_code=201)
def add_issue(issue: NewIssue):
    return db.insert_issue(issue.title)

@app.patch("/api/issues/{issue_id}/status")
def set_status(issue_id: int, body: StatusUpdate):
    if body.status not in ("open", "done"):
        raise HTTPException(400, "status must be 'open' or 'done'")
    if db.get_issue(issue_id) is None:
        raise HTTPException(404, "no such issue")
    return db.update_status(issue_id, body.status)


@app.delete("/api/issues/{issue_id}", status_code=204)
def delete_issue(issue_id: int):
    if db.get_issue(issue_id) is None:
        raise HTTPException(404, "no such issue")
    db.delete_issue(issue_id)
    return Response(status_code=204)
