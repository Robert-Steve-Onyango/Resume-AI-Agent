import psycopg2

# Update these values with your PostgreSQL credentials
DB_NAME = "Artieno"
DB_USER = "Artieno_admin"
DB_PASSWORD = "12345678"
DB_HOST = "localhost"
DB_PORT = "5432"

def create_resumes_table():
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS resumes (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            content TEXT NOT NULL
        )
    ''')
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    create_resumes_table()
    print("Table 'resumes' created (if not exists) in PostgreSQL.")
