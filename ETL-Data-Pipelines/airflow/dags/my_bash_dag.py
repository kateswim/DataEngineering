# Import the libraries
from datetime import timedelta
import os
# The DAG object; we'll need this to instantiate a DAG
from airflow.models import DAG
# Operators; you need this to write tasks!
from airflow.operators.bash import BashOperator
# This makes scheduling easy
from airflow.utils.dates import days_ago

# Define the path for the input and output files
# Using absolute paths for better reliability
base_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(os.path.dirname(base_dir), 'data')
os.makedirs(data_dir, exist_ok=True)

input_file = '/etc/passwd'
extracted_file = os.path.join(data_dir, 'extracted-data.txt')
transformed_file = os.path.join(data_dir, 'transformed.txt')
output_file = os.path.join(data_dir, 'data_for_analytics.csv')

# You can override them on a per-task basis during operator initialization
default_args = {
    'owner': 'Your name',
    'start_date': days_ago(0),
    'email': ['your email'],
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
dag = DAG(
    'my-first-bash-etl-dag',
    default_args=default_args,
    description='ETL DAG using Bash commands',
    schedule_interval=timedelta(days=1),
)

# Define the task 'extract' - extracts fields 1, 3, and 6 from /etc/passwd
extract = BashOperator(
    task_id='extract',
    bash_command=f'''
    echo "Inside Extract"
    awk -F: 'NF >= 6 {{print $1":"$3":"$6}}' {input_file} > {extracted_file}
    ''',
    dag=dag,
)

# Define the task 'transform' - converts colons to commas
transform = BashOperator(
    task_id='transform',
    bash_command=f'''
    echo "Inside Transform"
    sed 's/:/,/g' {extracted_file} > {transformed_file}
    ''',
    dag=dag,
)

# Define the task 'load' - copies transformed data to output CSV
load = BashOperator(
    task_id='load',
    bash_command=f'''
    echo "Inside Load"
    cp {transformed_file} {output_file}
    ''',
    dag=dag,
)

# Define the task 'check' - displays the final output
check = BashOperator(
    task_id='check',
    bash_command=f'''
    echo "Inside Check"
    cat {output_file}
    ''',
    dag=dag,
)

# Task pipeline
extract >> transform >> load >> check