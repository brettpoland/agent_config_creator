Agent Coding Config Creator

Build and run

Prerequisites
- Windows machine
- Python 3.11+ (virtualenv recommended)

Quick start (PowerShell)

```powershell
# create venv (if not already)
python -m venv .venv
& .venv/Scripts/Activate.ps1
python -m pip install -r requirements.txt

# run app
& .venv/Scripts/python.exe config_app.py

# build standalone exe (no console window)
& .venv/Scripts/Activate.ps1
& .\build_exe.ps1
# result: dist\config_app.exe
```

Notes
- The build script converts the provided PNG in `img/` to `img/app.ico` and embeds it; `img/app.ico` is present in the repo.
- The build uses PyInstaller's `--noconsole` option so the executable runs without an attached console window.
- If distributing the exe to other machines, ensure the target has the appropriate MSVC runtime.
- CI: consider adding a GitHub Actions workflow to build artifacts on push.
