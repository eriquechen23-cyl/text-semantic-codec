# CODEX.md

This directory contains the FastAPI backend that exposes the semantic codec as HTTP endpoints.

## Deployment

Render uses the root `render.yaml` service named `text-semantic-codec-api`.

## Local Development

Install dependencies from the repository root:

```bash
pip install -r backend/requirements.txt
uvicorn backend.main:app --reload
```
