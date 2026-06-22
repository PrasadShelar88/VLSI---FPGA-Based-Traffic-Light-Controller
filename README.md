# FPGA-Based Traffic Light Controller

## 📌 Project Overview

This project is a **VLSI Course Project** based on an **FPGA-Based Traffic Light Controller**. It is designed using the concept of a **Finite State Machine (FSM)** to control traffic signals for a 4-way intersection.

The project includes a **Virtual FPGA FSM Simulator** with a frontend dashboard and FastAPI backend. It simulates North-South and East-West traffic lights, pedestrian request, emergency all-red mode, night blinking mode, simulation logs, CSV/PDF reports, RTL access, and Verilog testbench access.

This project is useful for understanding FPGA-based digital control systems, Verilog RTL design, FSM implementation, and simulation-based verification.

---

## 🎯 Objective

The objective of this project is to design and simulate a traffic light controller using FPGA and Verilog concepts.

The system controls:

* North-South traffic signal
* East-West traffic signal
* Pedestrian crossing signal
* Emergency all-red mode
* Night blinking mode
* FSM-based state transitions
* Safety condition checking

---

## 🧠 What is an FPGA-Based Traffic Light Controller?

An FPGA-Based Traffic Light Controller is a digital control system that uses hardware logic to manage traffic signal timing and state transitions.

Instead of using software-only control, the logic is designed using Verilog and can be implemented on an FPGA board. Traffic lights are controlled using FSM states such as:

* NS_GREEN
* NS_YELLOW
* ALL_RED
* EW_GREEN
* EW_YELLOW
* PEDESTRIAN_WALK
* EMERGENCY_ALL_RED
* NIGHT_BLINK

---

## 🚦 Features

* Virtual FPGA traffic light FSM simulator
* North-South and East-West signal control
* Pedestrian request support
* Emergency all-red safety mode
* Night blinking mode
* State-by-state simulation timeline
* Safety check to avoid conflicting green signals
* Backend API using FastAPI
* Frontend dashboard using HTML, CSS, and JavaScript
* CSV report generation
* PDF report generation
* RTL Verilog source access
* Verilog testbench access
* GitHub-ready project structure

---

## 🛠️ Technologies Used

### VLSI / FPGA

* Verilog HDL
* RTL design
* Finite State Machine
* Testbench verification
* Traffic signal timing logic

### Backend

* Python
* FastAPI
* Uvicorn
* ReportLab
* CSV logging

### Frontend

* HTML
* CSS
* JavaScript
* Python HTTP Server

### Tools

* VS Code
* PowerShell
* Browser
* GitHub
* Optional: Vivado / ModelSim / Icarus Verilog

---

## 🧩 VLSI Concepts Used

This project demonstrates the following VLSI and digital design concepts:

* Finite State Machine design
* Sequential logic
* Combinational logic
* Clock-based state transition
* Reset logic
* Counters and timers
* Verilog RTL coding
* Testbench creation
* Simulation-based verification
* Safety checking
* FPGA LED output mapping concept

---

## 🏗️ System Architecture

```text
User Inputs
    |
    v
Frontend Dashboard
    |
    v
FastAPI Backend
    |
    v
FSM Simulation Engine
    |
    v
Traffic Light State Logic
    |
    v
Simulation Output + Logs + Reports
    |
    v
RTL / Testbench Access
```

---

## 🚥 FSM State Flow

```text
NS_GREEN
   |
   v
NS_YELLOW
   |
   v
ALL_RED_1
   |
   v
EW_GREEN
   |
   v
EW_YELLOW
   |
   v
ALL_RED_2
   |
   v
NS_GREEN
```

Additional modes:

```text
Pedestrian Request  -> PED_WALK
Emergency Input     -> EMERGENCY_ALL_RED
Night Mode          -> NIGHT_BLINK
```

---

## 📊 FSM State Table

| State             | North-South Signal | East-West Signal | Pedestrian Signal | Description                  |
| ----------------- | ------------------ | ---------------- | ----------------- | ---------------------------- |
| NS_GREEN          | Green              | Red              | Don't Walk        | North-South traffic moves    |
| NS_YELLOW         | Yellow             | Red              | Don't Walk        | North-South prepares to stop |
| ALL_RED_1         | Red                | Red              | Don't Walk        | Safety gap before EW green   |
| EW_GREEN          | Red                | Green            | Don't Walk        | East-West traffic moves      |
| EW_YELLOW         | Red                | Yellow           | Don't Walk        | East-West prepares to stop   |
| ALL_RED_2         | Red                | Red              | Don't Walk        | Safety gap before NS green   |
| PED_WALK          | Red                | Red              | Walk              | Pedestrians can cross        |
| EMERGENCY_ALL_RED | Red                | Red              | Don't Walk        | Emergency safety mode        |
| NIGHT_BLINK       | Blink              | Blink            | Don't Walk        | Night traffic mode           |

---

## 🖥️ Frontend Dashboard

The frontend dashboard allows the user to:

* Test backend connection
* Run FSM simulation
* Select start state
* Set green/yellow/all-red/walk time
* Enable vehicle sensors
* Enable pedestrian request
* Enable emergency mode
* Enable night blink mode
* View live traffic signals
* View simulation timeline
* Download CSV and PDF reports
* View RTL and testbench source code

---

## ⚙️ Backend API

The backend provides APIs for:

* Running FSM simulation
* Returning latest simulation status
* Saving simulation logs
* Downloading CSV report
* Downloading PDF report
* Viewing RTL code
* Viewing testbench code
* Clearing logs

---

## 📁 Folder Structure

```text
FPGA-Traffic-Light-Controller/
│
├── fpga_traffic_light_backend/
│   ├── main.py
│   ├── requirements.txt
│   ├── run_backend.bat
│   ├── rtl/
│   │   └── traffic_light_controller.v
│   ├── tb/
│   │   └── traffic_light_tb.v
│   ├── reports/
│   └── README.md
│
├── fpga_traffic_light_frontend/
│   ├── index.html
│   ├── assets/
│   │   ├── styles.css
│   │   └── app.js
│   ├── run_frontend.bat
│   └── README.md
│
├── screenshots/
│   ├── dashboard.png
│   ├── simulation_output.png
│   ├── timeline.png
│   ├── rtl_code.png
│   └── testbench_code.png
│
└── README.md
```

---

## ▶️ How to Run Backend

Open PowerShell:

```powershell
cd "C:\Projects\VLSI\fpga_traffic_light_backend"

py -3.10 -m venv .venv

.\.venv\Scripts\activate

python -m pip install --upgrade pip

pip install -r requirements.txt

python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

Backend will run at:

```text
http://127.0.0.1:8000
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

---

## ▶️ How to Run Frontend

Open a new PowerShell window:

```powershell
cd "C:\Projects\VLSI\fpga_traffic_light_frontend"

py -3.10 -m http.server 5500 --bind 127.0.0.1
```

Open in browser:

```text
http://127.0.0.1:5500/index.html
```

---

## ✅ Sample Simulation Output

Example output:

```text
Simulation completed. Safety check: PASS

Current State: EW_GREEN

North-South Signal: RED
East-West Signal: GREEN
Pedestrian Signal: DON'T WALK

Safety Check: PASS
```

Example timeline:

```text
NS_GREEN -> NS_YELLOW -> ALL_RED_1 -> EW_GREEN
```

---

## 🔐 Safety Check

The system checks that both directions are never green at the same time.

Unsafe condition:

```text
NS_GREEN and EW_GREEN at the same time
```

Expected safe condition:

```text
Only one direction should be GREEN at a time.
```

If the FSM works correctly, the dashboard shows:

```text
Safety Check: PASS
```

---

## 📄 Reports

The project supports:

* CSV simulation log report
* PDF simulation report
* FSM state timeline
* Safety result
* Final state output

These reports can be downloaded from the frontend dashboard.

---

## 💻 RTL Source Code

The project includes Verilog RTL code for the traffic light controller.

RTL code represents the actual digital hardware logic that can be simulated or implemented on an FPGA board.

Main RTL module:

```text
traffic_light_controller.v
```

---

## 🧪 Testbench

The project includes a Verilog testbench to verify the RTL design.

The testbench checks:

* Clock behavior
* Reset behavior
* FSM transitions
* Traffic signal outputs
* Safety condition
* Simulation waveform generation

Testbench file:

```text
traffic_light_tb.v
```

---


## 🚀 Future Improvements

This project can be improved further by adding:

* Countdown timer display
* Real-time clock-based night mode
* Adaptive traffic control using vehicle density
* Multiple junction support
* UART/SPI communication
* FPGA board LED implementation
* Formal verification using assertions
* 7-segment display for state/timer
* IoT-based smart traffic monitoring

---

## 🎓 Learning Outcomes

From this project, I learned:

* How to design a traffic light controller using FSM
* How FPGA-based control logic works
* How to write Verilog RTL code
* How to create a Verilog testbench
* How to verify FSM transitions
* How to check safety conditions in digital logic
* How to build a FastAPI backend for simulation
* How to create a frontend dashboard for VLSI projects
* How to generate CSV and PDF reports
* How to prepare a GitHub-ready engineering project

---

## 💬 Interview Questions and Answers

### 1. Explain your FPGA-Based Traffic Light Controller project.

This project is a traffic light controller designed using Verilog and FSM concepts. It controls North-South and East-West traffic signals using predefined timing states such as green, yellow, and red. The project also includes pedestrian request, emergency all-red mode, night blink mode, simulation logs, reports, RTL code, and testbench access.

### 2. Why did you use FSM in this project?

A traffic light controller works through a fixed sequence of states. FSM is suitable because each traffic condition can be represented as a state, and the controller moves from one state to another based on timing and input conditions.

### 3. What are the main states in your FSM?

The main states are NS_GREEN, NS_YELLOW, ALL_RED_1, EW_GREEN, EW_YELLOW, ALL_RED_2, PED_WALK, EMERGENCY_ALL_RED, and NIGHT_BLINK.

### 4. What is RTL?

RTL stands for Register Transfer Level. It describes how data moves between registers and how digital logic behaves in hardware.

### 5. What is the role of a testbench?

A testbench is used to verify the RTL design. It provides input signals like clock, reset, sensors, and emergency inputs, then checks whether the output is correct.

### 6. What is the purpose of the all-red state?

The all-red state ensures safety by keeping both directions red for a short time before switching traffic flow from one direction to another.

### 7. What is emergency all-red mode?

Emergency all-red mode forces all traffic signals to red. This is useful for emergency vehicle priority or unsafe situations.

### 8. What is night blink mode?

Night blink mode simulates low-traffic night operation where signals blink instead of following the normal full traffic cycle.

### 9. How did you verify the project?

I verified the project using a virtual FSM simulator, simulation timeline, safety checks, RTL code, testbench code, and generated reports.

### 10. How can this project be implemented on FPGA hardware?

The RTL code can be added to an FPGA design tool like Vivado. Traffic signal outputs can be mapped to FPGA LEDs using a constraints file, and input switches/buttons can be used for sensors, pedestrian request, emergency, and night mode.

---

## 🏁 Conclusion

The FPGA-Based Traffic Light Controller is a beginner-friendly and industry-relevant VLSI project. It demonstrates FSM-based digital design, Verilog RTL coding, testbench verification, simulation, safety checking, and GitHub-ready documentation.

This project can be used as a strong proof-of-work project for VLSI, FPGA, digital design, and embedded systems learning.
