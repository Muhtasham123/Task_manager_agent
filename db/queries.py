from db.connection import conn, cursor

def insert_task(task : dict):
    try:
        cursor.execute("""
        INSERT INTO tasks(title, description, category, priority, due_time)
        VALUES(%s, %s, %s, %s, %s)
        """,(
            task['title'],
            task['description'],
            task['category'],
            task['priority'],
            task['due_time']
        ))
        conn.commit()
        return cursor.lastrowid
    except Exception as e:
        print("Error inserting task : ",e)
