@echo off
cd /d "%~dp0"
echo Starting FPGA Traffic Light Controller backend...
echo Backend URL: http://127.0.0.1:8000
py -3.10 -m pip install -r requirements.txt
py -3.10 -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
pause
