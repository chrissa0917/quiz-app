# Flask Deployment Entrypoint Fix

This repository now includes a root Flask entrypoint so cloud platforms can auto-detect and start the app.

## Entrypoint

- Root file: `app.py`
- WSGI app object: `app`
- Templates: `templates/`

Most hosts that look for `app.py`, `main.py`, or `server.py` will now detect this project correctly.

## Required files for deployment

- `app.py` (Flask app exposed as `app`)
- `requirements.txt` (Python dependencies)
- `Procfile` (explicit process command for hosts that support it)

## Deploy commands

### Generic Python host

Install dependencies:

```bash
pip install -r requirements.txt
```

Start command:

```bash
gunicorn app:app
```

### Local run

```bash
pip install -r requirements.txt
python app.py
```

The app binds to `PORT` when provided by the host, otherwise defaults to `10000`.
