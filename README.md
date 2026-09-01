
# CPU Scheduling Simulator

A modular CPU scheduling simulator written in Python, with a PySide6 GUI for configuring workloads, comparing scheduling algorithms, and visualizing execution timelines.

The project focuses on the backend scheduling and simulation engine, with a separate GUI layer built on top.

## Features

* Modular scheduler architecture using a common scheduler interface
* FCFS scheduling
* SJF scheduling
* SRTF scheduling
* Round Robin with configurable quantum
* Preemptive and non-preemptive scheduling
* Process and workload modeling
* Discrete time-step simulation
* Ready queue and process state management
* Execution timeline generation
* Waiting time and turnaround time
* CPU utilization
* Algorithm comparison
* Input validation
* Automated testing with pytest
* PySide6 GUI
* Matplotlib Gantt chart visualization
## Technologies

- **Python 3.14** - Core programming language
- **PySide6** - Graphical user interface
- **Matplotlib** - Gantt chart visualization
- **Git and GitHub** - Version control and project hosting
## Architecture

The application uses a modular layered architecture.

### GUI Layer

Located in `src/gui/`, this layer provides the PySide6 interface. It allows users to:

- Add and remove processes
- Enter arrival and burst times
- Select scheduling algorithms
- Configure the Round Robin quantum
- View metrics and Gantt charts

### Model Layer

Located in `src/model/`, this layer defines the core data structures:

- `Process`: stores process information and execution state
- `Workload`: stores and validates processes
- `IORequest`: represents an I/O operation requested by a process

### Scheduling Layer

Located in `src/scheduler_algorithms/`, this layer contains the scheduling strategies:

- First-Come, First-Served
- Shortest Job First
- Shortest Remaining Time First
- Round Robin

Each algorithm follows the common `SchedulerInterface`.

### Simulation Layer

The `Simulator` coordinates the simulation by managing:

- Process arrivals
- Ready queues
- CPU execution
- Scheduling decisions
- Preemption
- Process completion
- I/O device activity

### Metrics Layer

Located in `src/metrics/`, this layer calculates:

- Waiting time
- Turnaround time
- CPU utilization

The `Comparison` class runs the same workload independently with each selected algorithm.

### Visualization Layer

Located in `src/visualization/`, this layer displays:

- CPU Gantt charts
- I/O Gantt charts
- Algorithm comparison tables

### Simulation Flow

    1. The GUI collects the workload and selected algorithms.
    2. The workload is validated.
    3. `Comparison` creates an independent simulation for each algorithm.
    4. `Simulator` executes each workload.
    5. A `SimulationResult` stores timelines and completed processes.
    6. `Metrics` calculates performance values.
    7. The GUI displays the results and Gantt charts.

## Project Structure

    ```text
    cpu-scheduler-simulator/
    ├── src/
    │   ├── devices/
    │   ├── gui/
    │   ├── metrics/
    │   ├── model/
    │   ├── scheduler_algorithms/
    │   ├── visualization/
    │   └── simulator.py
    ├── requirements.txt
    └── README.md
    ```

## Usage

1. Add processes with their arrival and burst times.
2. Select one or more scheduling algorithms.
3. Set the Round Robin quantum if required.
4. Click **Run**.
5. Review the metrics and Gantt chart results.
6. Click **Reset** to start another simulation.

## Installation on Linux
Clone the repository and enter the project directory:

```bash
git clone <repository-url>
cd Schedscope/cpu-scheduler-simulator
```

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the project dependencies:

```bash
python -m pip install -r requirements.txt
```

### Running on Linux

Start the graphical application from the project root:

```bash
python -m src.gui.main_window
```

## Installation on Windows

Clone the repository and enter the project directory:

```powershell
git clone <repository-url>
cd Schedscope\cpu-scheduler-simulator
```

Create and activate a virtual environment:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install the project dependencies:

```powershell
python -m pip install -r requirements.txt
```

### Running on Windows

Start the graphical application from the project root:

```powershell
python -m src.gui.main_window
```

If PowerShell blocks script activation, run the application directly instead:

```powershell
.\.venv\Scripts\python.exe -m src.gui.main_window
```
