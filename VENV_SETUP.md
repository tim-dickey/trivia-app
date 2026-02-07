# Virtual Environment Setup

## Overview
A Python virtual environment has been created and configured for the trivia-app project. All dependencies are isolated from the global Python installation.

## Virtual Environment Location
```
c:\Users\tdick\OneDrive\Documents\GitHub\trivia-app\venv\
```

## Setup Details

### Created
- **Date**: January 27, 2026
- **Python Version**: 3.13.9
- **Activation Command**: `.\venv\Scripts\Activate.ps1`

### Dependencies Installed
All dependencies from `backend/requirements.txt` have been successfully installed:

#### Core Framework
- FastAPI 0.104.1
- Uvicorn 0.24.0 (with standard extras)
- Starlette 0.27.0
- Python-multipart 0.0.6

#### Database
- SQLAlchemy 2.0.46 (upgraded from 2.0.23 for Python 3.13 compatibility)
- Alembic 1.12.1
- Psycopg 3.3.2 with binary support

#### Authentication & Security
- python-jose 3.3.0 (with cryptography)
- passlib 1.7.4 (with bcrypt)
- cryptography 46.0.3

#### Task Queue
- Celery 5.3.4
- Redis 5.0.1
- Kombu 5.6.2
- Billiard 4.2.4

#### Validation & Settings
- Pydantic 2.12.5 (upgraded from 2.5.0 for Python 3.13 compatibility)
- pydantic-settings 2.12.0 (upgraded from 2.1.0 for Python 3.13 compatibility)
- pydantic-core 2.41.5

#### Testing
- pytest 7.4.3
- pytest-asyncio 0.21.1
- pytest-cov 4.1.0
- httpx 0.25.1
- coverage 7.13.2

#### Development & Code Quality
- ruff 0.1.6
- black 23.11.0

### Configuration

#### VS Code Settings
Updated `.vscode/settings.json` to use the virtual environment:
```json
"python.defaultInterpreterPath": "${workspaceFolder}/venv/Scripts/python.exe"
```

#### Python Analysis
- Type checking mode: basic
- Extra paths configured for backend module

## Usage

### Activate the Virtual Environment
```powershell
# Windows (PowerShell)
.\venv\Scripts\Activate.ps1

# Windows (Command Prompt)
.\venv\Scripts\activate.bat

# Linux/macOS
source venv/bin/activate
```

### Install New Dependencies
```bash
# With virtual environment activated
pip install <package_name>

# Update requirements.txt
pip freeze > backend/requirements.txt
```

### Deactivate the Virtual Environment
```bash
deactivate
```

### Run the Application
```bash
# Make sure virtual environment is activated
cd backend
uvicorn main:app --reload
```

### Run Tests
```bash
# Make sure virtual environment is activated
pytest
```

## Notes

- **Naming Convention**: This project uses `venv/` as the standard virtual environment directory name (NOT `.venv/`). Please use `python -m venv venv` to maintain consistency.
- **Global Installation**: The global Python installation has NOT been modified. All dependencies are isolated in the venv directory.
- **Compatibility**: SQLAlchemy and Pydantic were upgraded to versions compatible with Python 3.13.
- **.gitignore**: The `venv/` directory is already configured in `.gitignore` and will not be committed to the repository.
- **VSCode**: Close and reopen VSCode or use the Python: Select Interpreter command to pick up the new virtual environment.

## Troubleshooting

### Virtual environment not activating
- Ensure you're in the project root directory
- On Windows, you may need to run: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

### Module not found errors
- Ensure the virtual environment is activated
- Verify the module is installed: `pip list | grep module_name`
- Reinstall if needed: `pip install -r backend/requirements.txt`

### Stale Python interpreter in VS Code
- Use `Ctrl+Shift+P` and run "Python: Select Interpreter"
- Choose the interpreter from `./venv/Scripts/python.exe`
