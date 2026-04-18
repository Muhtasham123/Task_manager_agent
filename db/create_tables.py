import db.connection
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
        status varchar(255) DEFAULT "pending",
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS drafts(
            id INT PRIMARY KEY AUTO_INCREMENT,
            title VARCHAR(255) UNIQUE,
            text TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
        )
        """
    )
    conn.commit()

create_tables()