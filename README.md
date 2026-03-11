<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0,1a1a2e,2e4a7a&height=200&section=header&text=Elevator%20Simulation&fontSize=52&fontColor=ffffff&fontAlignY=38&desc=Concurrent%20elevator%20system%20with%20real-time%20Pygame%20visualization&descAlignY=58&descSize=16" />

<br/>

![Python](https://img.shields.io/badge/Python-3.11-1a1a2e?style=for-the-badge&logo=python&logoColor=white)
![Pygame](https://img.shields.io/badge/GUI-Pygame-2e4a7a?style=for-the-badge&logo=python&logoColor=white)
![Threading](https://img.shields.io/badge/Concurrency-Threading-6b7280?style=for-the-badge&logo=python&logoColor=white)
![Status](https://img.shields.io/badge/Estado-Completado-2e4a7a?style=flat-square&labelColor=1a1a1a&color=2e4a7a)
![Universidad](https://img.shields.io/badge/PUCV-Hardware%20%26%20OS-3d3d3d?style=flat-square)

</div>

<br/>

<img src="https://capsule-render.vercel.app/api?type=rect&color=2e4a7a&height=2&section=header" />

### ▎DESCRIPTION

**Elevator Simulation** is a concurrent elevator system simulation for a 10-floor building. Developed in **Python 3** with real-time graphical visualization using **Pygame**, applying **Operating Systems** concepts such as threads and semaphores to manage elevator synchronization and passenger flow.

Each elevator runs on its own thread and coordinates access to shared resources using semaphores, preventing race conditions while transporting passengers to their destinations.

<br/>

<img src="https://capsule-render.vercel.app/api?type=rect&color=2e4a7a&height=2&section=header" />

### ▎FEATURES

- **Multi-elevator management** — configurable number of elevators running concurrently on independent threads.
- **Semaphore synchronization** — prevents race conditions when multiple elevators access shared passenger data.
- **Random passenger generation** — passengers are assigned random destination floors at runtime.
- **Cooldown system** — passengers wait on their floor before returning to ground level.
- **Real-time visualization** — live Pygame window showing elevators, passengers and floor states with color-coded status.
- **File-based configuration** — all simulation parameters loaded from an external `.txt` file.

<br/>

<img src="https://capsule-render.vercel.app/api?type=rect&color=2e4a7a&height=2&section=header" />

### ▎TECHNOLOGIES

| Technology | Usage |
|---|---|
| ![](https://img.shields.io/badge/Python%203-1a1a2e?style=flat-square&logo=python&logoColor=white) | Main language |
| ![](https://img.shields.io/badge/Pygame-2e4a7a?style=flat-square&logo=python&logoColor=white) | Real-time graphical visualization |
| ![](https://img.shields.io/badge/Threading-6b7280?style=flat-square) | Concurrent elevator execution |
| ![](https://img.shields.io/badge/Semaphores-1a1a2e?style=flat-square) | Shared resource synchronization |
| ![](https://img.shields.io/badge/File%20I%2FO-2e4a7a?style=flat-square) | Parameter loading from .txt |

<br/>

<img src="https://capsule-render.vercel.app/api?type=rect&color=2e4a7a&height=2&section=header" />

### ▎PREVIEW

| Initial State | Elevators Ascending |
|---|---|
| ![Initial](screenshots/01_initial_state.png) | ![Ascending](screenshots/02_elevators_ascending.png) |

| Passengers Descending | Mid Simulation |
|---|---|
| ![Descending](screenshots/03_passengers_descending.png) | ![Mid](screenshots/04_mid_simulation.png) |

<br/>

<img src="https://capsule-render.vercel.app/api?type=rect&color=2e4a7a&height=2&section=header" />

### ▎COLOR LEGEND

| Color | Meaning |
|---|---|
| 🟢 Green | Passenger waiting for elevator / riding up |
| 🟡 Yellow | Passenger riding down |
| 🔴 Red | Passenger on cooldown (waiting on floor) |

<br/>

<img src="https://capsule-render.vercel.app/api?type=rect&color=2e4a7a&height=2&section=header" />

### ▎PROJECT STRUCTURE

```
elevator-simulation/
├── main.py                  # Main simulation logic
├── datosascensores.txt      # Input configuration file
├── .gitignore
├── LICENSE
└── README.md
```

<br/>

<img src="https://capsule-render.vercel.app/api?type=rect&color=2e4a7a&height=2&section=header" />

### ▎CONFIGURATION FILE

Edit `datosascensores.txt` with your simulation parameters:

```
2       ← Number of elevators
5       ← Elevator capacity (max passengers)
20      ← Total number of passengers
5       ← Passengers generated per cycle
1       ← Time on floor 1
2       ← Time on floor 2
3       ← Time on floor 3
4       ← Time on floor 4
5       ← Time on floor 5
6       ← Time on floor 6
7       ← Time on floor 7
8       ← Time on floor 8
9       ← Time on floor 9
10      ← Time on floor 10
```

<br/>

<img src="https://capsule-render.vercel.app/api?type=rect&color=2e4a7a&height=2&section=header" />

### ▎REQUIREMENTS

- **Python 3.11** — [Download](https://www.python.org/downloads/release/python-3119/) ⚠️ Python 3.12+ is not supported by Pygame yet
- **Pygame** library

<br/>

<img src="https://capsule-render.vercel.app/api?type=rect&color=2e4a7a&height=2&section=header" />

### ▎HOW TO RUN

**1. Install dependencies**
```bash
pip install pygame
```

**2. Run the simulation**

Linux / macOS:
```bash
python main.py
```
Windows:
```bash
py -3.11 main.py
```

<br/>

<img src="https://capsule-render.vercel.app/api?type=rect&color=2e4a7a&height=2&section=header" />

### ▎ACADEMIC CONTEXT

Project developed for **Hardware & Operating Systems** -INF2322- course at the [Pontificia Universidad Católica de Valparaíso (PUCV)](https://www.pucv.cl), 1st semester of Computer Engineering during 2024.

Concepts covered: concurrent programming, thread management, semaphore-based synchronization, real-time graphical simulation.

<br/>

<img src="https://capsule-render.vercel.app/api?type=rect&color=2e4a7a&height=2&section=header" />

### ▎AUTHOR

<div align="center">

[![cord0990](https://img.shields.io/badge/@cord0990-1a1a2e?style=for-the-badge&logo=github&logoColor=white)](https://github.com/cord0990)

</div>

<br/>

<img src="https://capsule-render.vercel.app/api?type=waving&color=0,1a1a2e,2e4a7a&height=100&section=footer" />
