# HOSPITAL PIPELINE 

An automated Data ETL (Extract, Transform, Load) Pipeline custom-built to manage, process, and analyze hospital datasets efficiently. The pipeline ensures data integrity by extracting raw records, transforming and cleaning them, and then systematically loading the structured data into various formats (CSV or Database). It also incorporates insightful reporting, automated data visualization, robust logging, and a dedicated task scheduling functionality.

##  Team Members
- **Aashish Mahat**
- **Angel Khanal**
- **Bipin Bista**
- **Gehendra Rai**

##  Features
- **Data Extraction (`pipeline/extract.py`)**: Responsible for importing and accumulating raw data sets for further processing.
- **Data Transformation (`pipeline/transform.py`)**: Sanitizes, structures, and refines the data to prevent inconsistencies and anomalies.
- **Data Loading & Storage (`pipeline/load.py`, `pipeline/storage_choice.py`)**: Saves cleaned data intelligently into optimized formats like CSV and directly updates the main database (`hospital.db`).
- **Log Management (`Logs/logger_setup.py`)**: Provides real-time and tracked logging mechanisms to monitor pipeline executions.
- **Task Scheduling (`scheduler.py`)**: Empowers the project with automated chron-jobs to run the data pipeline consistently without manual oversight.
- **Reporting & Analytics (`report/`)**: Generates comprehensive structured reports (`reportgeneration.py`) and illustrative graphs (`report/graph/graphs.py`) for stakeholders automatically.

##  How to Run

1. **Run the entire Pipeline manually:**
   Run the central application script to activate the entire ETL flow immediately.
   ```bash
   python main.py
   ```

2. **Run automatically with the Scheduler:**
   Run the following to leave the project consistently running automation jobs according to the predefined schedule interval.
   ```bash
   python scheduler.py
   ```

##  Project Structure 
```text
HOSPITAL_PYPELINE/
│
├── pipeline/             # Core ETL mechanisms
│   ├── extract.py        # Loading initial datasets
│   ├── transform.py      # Cleansing dataset 
│   ├── load.py           # Saving data implementations
│   └── storage_choice.py # Storage routing
│
├── report/               # Analytical Reporting 
│   ├── reportgeneration.py # Summary scripts
│   └── graph/graphs.py     # Graph generator
│
├── Logs/                 # Execution Logs
│   └── logger_setup.py   # Global logging configuration
│
├── main.py               # Main pipeline execution script
├── scheduler.py          # Job scheduling setup script
└── hospital.db           # Formed Database
```
