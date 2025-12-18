# ETL Data Pipeline with Apache Airflow

This project contains an ETL (Extract, Transform, Load) pipeline implemented using Apache Airflow.

## Project Structure

```
ETL-Data-Pipelines/
├── airflow/
│   ├── dags/
│   │   └── etl_dag.py          # Main DAG file
│   ├── logs/                   # Airflow logs directory
│   └── plugins/                # Custom plugins (optional)
├── DAG.py                      # Original DAG file (can be removed)
└── requirements.txt            # Python dependencies
```

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Initialize Airflow Database

```bash
# Set the AIRFLOW_HOME environment variable (optional, defaults to ~/airflow)
export AIRFLOW_HOME=$(pwd)/airflow

# Initialize the database
airflow db init
```

### 3. Create Airflow User (for web UI)

```bash
airflow users create \
    --username admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com \
    --password admin
```

### 4. Set Airflow Home (if not already set)

```bash
export AIRFLOW_HOME=$(pwd)/airflow
```

Or add it to your `~/.zshrc` or `~/.bashrc`:
```bash
echo 'export AIRFLOW_HOME=/Users/katehoncharova/Documents/GitHub/DataEngineering/ETL-Data-Pipelines/airflow' >> ~/.zshrc
source ~/.zshrc
```

## Running Airflow

### 1. Start the Airflow Scheduler (in one terminal)

```bash
cd /Users/katehoncharova/Documents/GitHub/DataEngineering/ETL-Data-Pipelines
export AIRFLOW_HOME=$(pwd)/airflow
airflow scheduler
```

### 2. Start the Airflow Webserver (in another terminal)

```bash
cd /Users/katehoncharova/Documents/GitHub/DataEngineering/ETL-Data-Pipelines
export AIRFLOW_HOME=$(pwd)/airflow
airflow webserver --port 8080
```

### 3. Access the Web UI

Open your browser and go to: `http://localhost:8080`

- Username: `admin`
- Password: `admin` (or the password you set)

## DAG Overview

The DAG `my-first-python-etl-dag` performs the following tasks:

1. **Extract**: Reads from `/etc/passwd` and extracts specific fields (username, UID, home directory)
2. **Transform**: Converts the colon-separated format to comma-separated format
3. **Load**: Saves the transformed data to a CSV file
4. **Check**: Prints the final output for verification

The tasks run in sequence: `extract → transform → load → check`

## Output Files

Output files are stored in `airflow/data/`:
- `extracted-data.txt`
- `transformed.txt`
- `data_for_analytics.csv`

## Troubleshooting

### DAG not showing in UI
- Make sure the DAG file is in `airflow/dags/` directory
- Check for syntax errors: `python airflow/dags/etl_dag.py`
- Restart the scheduler

### Permission errors
- Make sure you have read access to `/etc/passwd`
- Check write permissions for the `airflow/data/` directory

### Port already in use
- Change the port: `airflow webserver --port 8081`

## Notes

- The DAG is scheduled to run daily (`schedule_interval=timedelta(days=1)`)
- You can trigger it manually from the Airflow UI
- Logs are stored in `airflow/logs/`

