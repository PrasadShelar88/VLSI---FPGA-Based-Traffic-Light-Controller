# FPGA Traffic Light Controller Frontend

This is the static frontend dashboard for the VLSI project **FPGA-Based Traffic Light Controller**.

## Run Frontend

1. Start backend first on:

```text
http://127.0.0.1:8000
```

2. Open PowerShell in this folder and run:

```powershell
.\run_frontend.bat
```

Or run manually:

```powershell
cd "C:\Projects\VLSI\fpga_traffic_light_frontend"
py -3.10 -m http.server 5500
```

3. Open browser:

```text
http://127.0.0.1:5500
```

## Features

- Backend connection test
- NS/EW traffic signal visualization
- FSM simulation input form
- Pedestrian request mode
- Emergency all-red mode
- Night blinking mode
- Logs table
- CSV/PDF report download
- RTL Verilog viewer
- Testbench viewer
