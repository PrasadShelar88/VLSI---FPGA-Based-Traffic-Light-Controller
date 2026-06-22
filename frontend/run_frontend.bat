@echo off
cd /d "%~dp0"
echo Starting FPGA Traffic Light frontend at http://127.0.0.1:5500
echo Keep this window open while using the dashboard.
py -3.10 -m http.server 5500
pause
