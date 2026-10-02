import psycopg2

def init_db():
    try:
        conn = psycopg2.connect(
            dbname="careerpilot",
            user="postgres",
            password="postgres",
            host="127.0.0.1",
            port=5432
        )
        cur = conn.cursor()
        cur.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')
        conn.commit()
        print("Successfully connected to PostgreSQL 'careerpilot' database and enabled 'uuid-ossp' extension.")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error connecting/initializing DB: {e}")

if __name__ == "__main__":
    init_db()
