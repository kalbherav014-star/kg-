# NOVA v3.0

NOVA is a modular, local-first AI operating assistant for Windows 11. The
project combines a Cloudflare Pages-compatible web interface with a Python
3.12/FastAPI service for local AI, voice, vision, and desktop automation.

> Development status: Module 0 (project foundation). User-facing features are
> added one tested module at a time; unfinished features are not represented as
> working functionality.

## Architecture

- `frontend/` — static HTML, CSS, and ES modules deployable to Cloudflare Pages.
- `backend/` — Python application packages and dependency manifests.
- `database/` — local SQLite runtime location (database files are ignored).
- `docs/` — installation, architecture, operations, and API documentation.
- `tests/` — automated tests organized by application layer.

The browser interface and local FastAPI service are intentionally separate.
Cloudflare Pages hosts static assets; Windows-only automation and local models
run on the trusted workstation and are never moved into the browser.

## Requirements

- Windows 11
- Git 2.40+
- Python 3.12.x
- 16 GB RAM recommended

See [INSTALL.md](INSTALL.md) for the reproducible setup process and
[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for system boundaries.

## Development

```powershell
Copy-Item .env.example .env
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r backend/requirements-dev.txt
python -m pytest
python -m ruff check .
python -m mypy backend
```

Do not commit `.env`, SQLite databases, model weights, logs, or credentials.

## Deployment model

The frontend will be deployable from `frontend/` to Cloudflare Pages. The
FastAPI service is designed for the Windows workstation because browser and PC
automation require local operating-system access. Production deployments must
use HTTPS, explicit allowed origins, authenticated API access, and least
privilege.

## License

Licensed under the [MIT License](LICENSE).
