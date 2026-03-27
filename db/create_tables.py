from db.connection import conn, cursor

def create_tables():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks(
        id INT PRIMARY KEY AUTO_INCREMENT,
        title VARCHAR(255) UNIQUE,
        description TEXT,
        category VARCHAR(255),
        priority VARCHAR(255),
        due_time DATETIME NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()

create_tables()