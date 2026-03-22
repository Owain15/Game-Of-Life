@echo off
cd /d "%~dp0"
py -c "import flask" 2>nul || py -m pip install flask
start http://localhost:5000
py app.py
pause
