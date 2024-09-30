import psycopg2


# Database connection parameters
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASS = "1234"
DB_HOST = "postgres-db"
DB_PORT = "5432"


def get_postgres_connection():
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        host=DB_HOST,
        port=DB_PORT
    )
    return conn



def create_table_if_not_exist():
    conn = get_postgres_connection()
    cur = conn.cursor()

    # Create table if it doesn't exist
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
          id SERIAL PRIMARY KEY,
          email VARCHAR(255) UNIQUE NOT NULL
        );
    ''')
    
    conn.commit()

    cur.close()
    conn.close()

    print("Table 'users' checked and created if not existing.")
