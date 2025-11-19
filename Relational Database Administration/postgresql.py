import psycopg2

# ---------- Connection settings ----------
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "demo",      # your database name
    "user": "postgres",    # your username
    "password": "your_password_here"
}

def get_connection():
    return psycopg2.connect(**DB_CONFIG)

# ---------- Create table ----------
def create_table():
    sql = """
    CREATE TABLE IF NOT EXISTS bookings (
        id SERIAL PRIMARY KEY,
        customer_name VARCHAR(100),
        flight_no VARCHAR(10),
        created_at TIMESTAMP DEFAULT NOW()
    );
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
    print("Table created (or already exists).")

# ---------- Insert a row ----------
def insert_booking(customer_name, flight_no):
    sql = """
    INSERT INTO bookings (customer_name, flight_no)
    VALUES (%s, %s)
    RETURNING id;
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (customer_name, flight_no))
            new_id = cur.fetchone()[0]
    print(f"Inserted booking with id = {new_id}")

# ---------- Simple query ----------
def list_bookings():
    sql = "SELECT id, customer_name, flight_no, created_at FROM bookings ORDER BY id;"
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
            rows = cur.fetchall()
    for row in rows:
        print(row)

if __name__ == "__main__":
    create_table()
    insert_booking("Kate Honcharova", "SU123")
    insert_booking("John Doe", "LH456")
    print("Current bookings:")
    list_bookings()
