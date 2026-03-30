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


def update_task(id : str, updation_dict : dict):
    try:
        # buildint SET clause

        set_clause = ", ".join([f"{key} = %s" for key in updation_dict.keys()])

        final_query = f"UPDATE tasks SET {set_clause} WHERE id = %s"

        values = list(updation_dict.values()) + [id]

        cursor.execute(final_query, values)

        conn.commit()
        return True

    except Exception as e:
        print("Error updating task : ",e)
        return False


def delete_task(task_id : int):
    try:
        cursor.execute("""
        DELETE FROM tasks where id = %s
        """,(task_id,))

        conn.commit()

        return True
    except Exception as e:
        print("Error deleting task : ",e)
        return False
