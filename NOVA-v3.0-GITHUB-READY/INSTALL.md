# Installation

## 1. Install prerequisites

Install Git and the latest Python 3.12 release from their official sources.
During Python installation, enable the Python launcher and add Python to PATH.

Verify both tools in PowerShell:

```powershell
git --version
py -3.12 --version
```

## 2. Create the environment

From the repository root:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r backend/requirements-dev.txt
Copy-Item .env.example .env
```

If PowerShell blocks activation for the current process:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## 3. Verify the foundation

```powershell
python -m pytest
python -m ruff check .
python -m mypy backend
```

The web application and API run commands will be added with their respective
modules. Module 0 intentionally contains no pretend application server.

## Troubleshooting

- `py` is not recognized: reinstall Python 3.12 with the launcher enabled, then
  open a new PowerShell window.
- Dependency installation fails: confirm the virtual environment is active and
  `python --version` reports Python 3.12.
- Configuration fails: compare `.env` with `.env.example`; never add quotes
  unless they are intended to be part of a value.

