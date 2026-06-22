# FPGA Traffic Light Controller Backend

FastAPI backend for the **VLSI Course Project: FPGA-Based Traffic Light Controller**.

## Features

- Traffic light FSM simulation for North-South and East-West roads
- Vehicle sensor support
- Pedestrian request support
- Emergency all-red mode
- Night blinking mode
- CSV log download
- PDF report download
- Verilog RTL source endpoint
- Verilog testbench endpoint
- Beginner-friendly Windows run files

## Run on Windows PowerShell

```powershell
cd "C:\Projects\VLSI\fpga_traffic_light_backend"
py -3.10 -m venv .venv
.\.venv\Scriptsctivate
pip install -r requirements.txt
python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

## Important API Routes

| Route | Method | Purpose |
|---|---:|---|
| `/` | GET | Backend status |
| `/health` | GET | Connection test |
| `/simulate` | POST | Run traffic light simulation |
| `/logs` | GET | View saved simulation records |
| `/logs/clear` | DELETE | Clear logs |
| `/download/csv` | GET | Download CSV logs |
| `/download/pdf` | GET | Download PDF report |
| `/source/rtl` | GET | Download RTL Verilog |
| `/source/testbench` | GET | Download Verilog testbench |

## Sample JSON for `/simulate`

```json
{
  "cycles": 20,
  "ns_sensor": true,
  "ew_sensor": false,
  "pedestrian_request": false,
  "emergency": false,
  "night_mode": false,
  "green_time": 5,
  "yellow_time": 2,
  "all_red_time": 1,
  "walk_time": 4,
  "start_state": "NS_GREEN"
}
```

## Stop Backend

Press `CTRL + C` in the backend terminal.
