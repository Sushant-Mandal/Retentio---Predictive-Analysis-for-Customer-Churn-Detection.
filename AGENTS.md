# AGENTS.md — Retentio Resumption Instructions

## Read first

Before doing anything else, read:
1. `TASKS.md` — current task list and status
2. `DEBUG_STATE.md` — verified facts, completed work, current blocker, exact next action

## Rules

- Do NOT rescan the full repository. All relevant files are listed in DEBUG_STATE.md.
- Do NOT repeat successful checks (health check, login 401 test, process identification).
- Do NOT launch a duplicate backend server. PID 8460 owns port 8000.
- Do NOT delete any virtual environment without explicit user approval.
- Update `DEBUG_STATE.md` and `TASKS.md` after each meaningful step.
- Report each task as PASS, FAIL, or BLOCKED with brief evidence.

## Project Quick Reference

| Item | Value |
|------|-------|
| Backend root | `F:\Retentio\backend` |
| Frontend root | `F:\Retentio\retentio` |
| Backend entry | `backend/main.py` → uvicorn |
| Active venv | `backend/venv/Scripts/python.exe` |
| API base URL | `http://localhost:8000/api/v1` |
| Auth routes | `backend/api/routes/auth.py` |
| DB module | `backend/db/__init__.py` |
| Auth service | `backend/services/auth_service.py` |
| Schemas | `backend/schemas/__init__.py` |
| Frontend API client | `retentio/client/src/lib/api.ts` |
| Vite proxy | `/api → http://localhost:8000` |
