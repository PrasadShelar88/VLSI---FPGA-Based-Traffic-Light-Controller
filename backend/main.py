
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, PlainTextResponse
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Literal
from pathlib import Path
import csv
import json
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

BASE_DIR = Path(__file__).resolve().parent
LOG_DIR = BASE_DIR / "logs"
REPORT_DIR = BASE_DIR / "reports"
RTL_FILE = BASE_DIR / "rtl" / "traffic_light_controller.v"
TB_FILE = BASE_DIR / "tb" / "traffic_light_tb.v"
LOG_DIR.mkdir(exist_ok=True)
REPORT_DIR.mkdir(exist_ok=True)
CSV_FILE = LOG_DIR / "traffic_light_logs.csv"
JSON_FILE = LOG_DIR / "traffic_light_logs.json"
PDF_FILE = REPORT_DIR / "traffic_light_report.pdf"

app = FastAPI(
    title="FPGA-Based Traffic Light Controller Backend",
    description="FastAPI simulation backend for a VLSI FPGA Traffic Light Controller project.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

StateName = Literal[
    "NS_GREEN", "NS_YELLOW", "ALL_RED_1", "EW_GREEN", "EW_YELLOW",
    "ALL_RED_2", "PED_WALK", "EMERGENCY_ALL_RED", "NIGHT_BLINK"
]

class SimulationRequest(BaseModel):
    cycles: int = Field(default=20, ge=1, le=500)
    ns_sensor: bool = False
    ew_sensor: bool = True
    pedestrian_request: bool = False
    emergency: bool = False
    night_mode: bool = False
    green_time: int = Field(default=5, ge=1, le=60)
    yellow_time: int = Field(default=2, ge=1, le=20)
    all_red_time: int = Field(default=1, ge=1, le=20)
    walk_time: int = Field(default=4, ge=1, le=60)
    start_state: StateName = "NS_GREEN"

STATE_OUTPUTS = {
    "NS_GREEN": {"ns": "GREEN", "ew": "RED", "pedestrian": "DON'T WALK"},
    "NS_YELLOW": {"ns": "YELLOW", "ew": "RED", "pedestrian": "DON'T WALK"},
    "ALL_RED_1": {"ns": "RED", "ew": "RED", "pedestrian": "DON'T WALK"},
    "EW_GREEN": {"ns": "RED", "ew": "GREEN", "pedestrian": "DON'T WALK"},
    "EW_YELLOW": {"ns": "RED", "ew": "YELLOW", "pedestrian": "DON'T WALK"},
    "ALL_RED_2": {"ns": "RED", "ew": "RED", "pedestrian": "DON'T WALK"},
    "PED_WALK": {"ns": "RED", "ew": "RED", "pedestrian": "WALK"},
    "EMERGENCY_ALL_RED": {"ns": "RED", "ew": "RED", "pedestrian": "DON'T WALK"},
    "NIGHT_BLINK": {"ns": "BLINK_YELLOW", "ew": "BLINK_RED", "pedestrian": "DON'T WALK"},
}

DURATIONS = {
    "NS_GREEN": "green_time",
    "NS_YELLOW": "yellow_time",
    "ALL_RED_1": "all_red_time",
    "EW_GREEN": "green_time",
    "EW_YELLOW": "yellow_time",
    "ALL_RED_2": "all_red_time",
    "PED_WALK": "walk_time",
}


def next_state(state: str, req: SimulationRequest, timer: int, ped_latched: bool) -> str:
    if req.emergency:
        return "EMERGENCY_ALL_RED"
    if req.night_mode:
        return "NIGHT_BLINK"
    if state in {"EMERGENCY_ALL_RED", "NIGHT_BLINK"}:
        return "NS_GREEN"
    duration_key = DURATIONS.get(state)
    duration = getattr(req, duration_key) if duration_key else 1
    if timer < duration:
        return state
    if state == "NS_GREEN":
        return "NS_YELLOW" if (req.ew_sensor or ped_latched) else "NS_GREEN"
    if state == "NS_YELLOW":
        return "ALL_RED_1"
    if state == "ALL_RED_1":
        return "PED_WALK" if ped_latched else "EW_GREEN"
    if state == "EW_GREEN":
        return "EW_YELLOW" if (req.ns_sensor or ped_latched) else "EW_GREEN"
    if state == "EW_YELLOW":
        return "ALL_RED_2"
    if state == "ALL_RED_2":
        return "PED_WALK" if ped_latched else "NS_GREEN"
    if state == "PED_WALK":
        return "NS_GREEN"
    return "NS_GREEN"


def read_logs() -> List[Dict[str, Any]]:
    if not JSON_FILE.exists():
        return []
    try:
        return json.loads(JSON_FILE.read_text(encoding="utf-8"))
    except Exception:
        return []


def write_logs(records: List[Dict[str, Any]]) -> None:
    JSON_FILE.write_text(json.dumps(records, indent=2), encoding="utf-8")
    with CSV_FILE.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["timestamp", "cycle", "state", "ns", "ew", "pedestrian", "safe", "note"])
        writer.writeheader()
        for r in records:
            writer.writerow({k: r.get(k, "") for k in writer.fieldnames})


def make_pdf(records: List[Dict[str, Any]]) -> Path:
    c = canvas.Canvas(str(PDF_FILE), pagesize=A4)
    width, height = A4
    y = height - 50
    c.setFont("Helvetica-Bold", 15)
    c.drawString(40, y, "FPGA-Based Traffic Light Controller Report")
    y -= 30
    c.setFont("Helvetica", 10)
    c.drawString(40, y, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    y -= 25
    c.drawString(40, y, "Project: FSM-based Verilog traffic light controller with sensors, pedestrian request, emergency and night mode.")
    y -= 25
    c.setFont("Helvetica-Bold", 11)
    c.drawString(40, y, "Recent Simulation Records")
    y -= 20
    c.setFont("Helvetica", 9)
    if not records:
        c.drawString(40, y, "No simulation records available.")
    else:
        for r in records[-35:]:
            line = f"Cycle {r['cycle']:>3}: {r['state']:<18} NS={r['ns']:<12} EW={r['ew']:<12} PED={r['pedestrian']:<10} Safe={r['safe']}"
            c.drawString(40, y, line[:120])
            y -= 14
            if y < 50:
                c.showPage()
                y = height - 50
                c.setFont("Helvetica", 9)
    c.save()
    return PDF_FILE


@app.get("/")
def root():
    return {
        "project": "FPGA-Based Traffic Light Controller",
        "status": "Backend running",
        "docs": "http://127.0.0.1:8000/docs",
        "routes": ["/health", "/simulate", "/logs", "/download/csv", "/download/pdf", "/source/rtl", "/source/testbench"],
    }

@app.get("/health")
def health():
    return {"ok": True, "message": "FPGA Traffic Light Controller backend connected"}

@app.post("/simulate")
def simulate(req: SimulationRequest):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    state = req.start_state
    timer = 0
    ped_latched = req.pedestrian_request
    run_records = []
    for cycle in range(req.cycles):
        outputs = STATE_OUTPUTS[state]
        safe = not (outputs["ns"] == "GREEN" and outputs["ew"] == "GREEN")
        note = "OK"
        if state == "EMERGENCY_ALL_RED":
            note = "Emergency active: all-red fail-safe mode"
        elif state == "NIGHT_BLINK":
            note = "Night mode: blinking yellow/red pattern"
        elif state == "PED_WALK":
            note = "Pedestrian crossing served"
        record = {
            "timestamp": timestamp,
            "cycle": cycle,
            "state": state,
            "ns": outputs["ns"],
            "ew": outputs["ew"],
            "pedestrian": outputs["pedestrian"],
            "safe": safe,
            "note": note,
        }
        run_records.append(record)
        ns = next_state(state, req, timer + 1, ped_latched)
        if ns != state:
            timer = 0
            if state == "PED_WALK":
                ped_latched = False
        else:
            timer += 1
        state = ns
    all_records = read_logs() + run_records
    write_logs(all_records[-1000:])
    return {
        "message": "Simulation completed",
        "input": req.model_dump(),
        "total_cycles": req.cycles,
        "final_state": state,
        "safety_check": "PASS" if all(r["safe"] for r in run_records) else "FAIL",
        "records": run_records,
        "summary": {
            "normal_fsm_states": ["NS_GREEN", "NS_YELLOW", "ALL_RED_1", "EW_GREEN", "EW_YELLOW", "ALL_RED_2"],
            "special_modes": ["PED_WALK", "EMERGENCY_ALL_RED", "NIGHT_BLINK"],
            "verilog_ready": True,
        },
    }

@app.get("/logs")
def logs():
    records = read_logs()
    return {"count": len(records), "records": records[-100:]}

@app.delete("/logs/clear")
def clear_logs():
    write_logs([])
    return {"message": "Logs cleared"}

@app.get("/download/csv")
def download_csv():
    if not CSV_FILE.exists():
        write_logs([])
    return FileResponse(str(CSV_FILE), media_type="text/csv", filename="traffic_light_logs.csv")

@app.get("/download/pdf")
def download_pdf():
    pdf = make_pdf(read_logs())
    return FileResponse(str(pdf), media_type="application/pdf", filename="traffic_light_report.pdf")

@app.get("/source/rtl", response_class=PlainTextResponse)
def source_rtl():
    return RTL_FILE.read_text(encoding="utf-8")

@app.get("/source/testbench", response_class=PlainTextResponse)
def source_testbench():
    return TB_FILE.read_text(encoding="utf-8")
