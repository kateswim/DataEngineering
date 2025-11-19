#!/usr/bin/env python3
"""
Script to execute world_mysql_script.sql using mysql command-line tool.
"""

import subprocess
import sys
import os
from pathlib import Path

# ---------- Connection settings ----------
MYSQL_HOST = "localhost"
MYSQL_PORT = "3306"
MYSQL_USER = "root"
MYSQL_PASSWORD = ""  # No password for local MySQL

def run_sql_file_with_mysql(sql_file_path, database="world"):
    """
    Execute SQL file using mysql command-line tool.
    """
    sql_file = Path(sql_file_path)
    
    if not sql_file.exists():
        print(f"❌ Error: File {sql_file_path} not found!")
        return False
    
    # First, create the database if it doesn't exist
    print(f"Creating database '{database}' if it doesn't exist...")
    create_db_cmd = [
        'mysql',
        '-h', MYSQL_HOST,
        '-P', MYSQL_PORT,
        '-u', MYSQL_USER,
        '-e', f'CREATE DATABASE IF NOT EXISTS {database};'
    ]
    
    if MYSQL_PASSWORD:
        env = dict(os.environ)
        env['MYSQL_PWD'] = MYSQL_PASSWORD
    else:
        env = dict(os.environ)
    
    try:
        result = subprocess.run(
            create_db_cmd,
            env=env,
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            print(f"Warning: {result.stderr}")
    except Exception as e:
        print(f"Warning creating database: {e}")
    
    # Build mysql command to execute SQL file
    mysql_cmd = [
        'mysql',
        '-h', MYSQL_HOST,
        '-P', MYSQL_PORT,
        '-u', MYSQL_USER,
        database  # Specify database name
    ]
    
    print(f"Executing SQL file: {sql_file_path}")
    print(f"Connecting to MySQL at {MYSQL_HOST}:{MYSQL_PORT} as user {MYSQL_USER}")
    print(f"Loading into database: {database}")
    print("This may take a while...\n")
    
    try:
        with open(sql_file, 'r', encoding='utf-8') as f:
            result = subprocess.run(
                mysql_cmd,
                stdin=f,
                env=env,
                capture_output=True,
                text=True
            )
        
        if result.returncode == 0:
            print("✅ SQL file executed successfully!")
            if result.stdout:
                print("\nOutput:")
                print(result.stdout)
            return True
        else:
            print("❌ Error executing SQL file:")
            print(result.stderr)
            if result.stdout:
                print("\nOutput:")
                print(result.stdout)
            return False
            
    except FileNotFoundError:
        print("❌ Error: mysql command not found!")
        print("   Please make sure MySQL client tools are installed.")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    # Get SQL file path
    if len(sys.argv) > 1:
        sql_file = sys.argv[1]
    else:
        sql_file = Path(__file__).parent / "world_mysql_script.sql"
    
    success = run_sql_file_with_mysql(sql_file)
    sys.exit(0 if success else 1)

