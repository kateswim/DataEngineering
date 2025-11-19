#!/usr/bin/env python3
"""
Simple script to execute flights.sql using psql command-line tool.
This is the recommended way to run PostgreSQL dump files.
"""

import subprocess
import sys
import os
from pathlib import Path

# ---------- Connection settings ----------
# Update these values to match your PostgreSQL setup
PG_HOST = "172.21.241.152"
PG_PORT = "5432"
PG_USER = "postgres"
PG_PASSWORD = "WrFtl2aiBchKuZgVQKU3UrN4"

def run_sql_file_with_psql(sql_file_path):
    """
    Execute SQL file using psql command-line tool.
    This is the most reliable way to handle PostgreSQL dump files.
    """
    sql_file = Path(sql_file_path)
    
    if not sql_file.exists():
        print(f"❌ Error: File {sql_file_path} not found!")
        return False
    
    # Set PGPASSWORD environment variable for password authentication
    env = dict(os.environ)
    env['PGPASSWORD'] = PG_PASSWORD
    
    # Build psql command
    psql_cmd = [
        'psql',
        '-h', PG_HOST,
        '-p', PG_PORT,
        '-U', PG_USER,
        '-f', str(sql_file)
    ]
    
    print(f"Executing SQL file: {sql_file_path}")
    print(f"Connecting to PostgreSQL at {PG_HOST}:{PG_PORT} as user {PG_USER}")
    print("This may take a while for large files...\n")
    
    try:
        result = subprocess.run(
            psql_cmd,
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
        print("❌ Error: psql command not found!")
        print("   Please make sure PostgreSQL client tools are installed.")
        print("   On macOS: brew install postgresql")
        print("   On Ubuntu: sudo apt-get install postgresql-client")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    import os
    
    # Check if password is set
    if PG_PASSWORD == "your_password_here":
        print("⚠️  Please update PG_PASSWORD in this script!")
        print("   Edit this file and set PG_PASSWORD to your PostgreSQL password.")
        sys.exit(1)
    
    # Get SQL file path
    if len(sys.argv) > 1:
        sql_file = sys.argv[1]
    else:
        sql_file = Path(__file__).parent / "flights.sql"
    
    success = run_sql_file_with_psql(sql_file)
    sys.exit(0 if success else 1)

