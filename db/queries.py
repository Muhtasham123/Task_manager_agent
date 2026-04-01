from db.connection import conn, cursor, r
import json

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

        task_id = cursor.lastrowid

        conn.commit()

        if task_id:
            r.xadd("task_events", {
                "event_type" : "CREATE_TASK",
                "task_id" : task_id
            })

        return task_id
    except Exception as e:
        print("Error inserting task : ",e)


def update_task(id : str, updation_dict : dict, metadata : dict):
    try:
        # buildint SET clause

        set_clause = ", ".join([f"{key} = %s" for key in updation_dict.keys()])

        final_query = f"UPDATE tasks SET {set_clause} WHERE id = %s"

        values = list(updation_dict.values()) + [id]

        cursor.execute(final_query, values)

        conn.commit()

        rowcount = cursor.rowcount

        if rowcount:
            r.xadd("task_events", {
                "event_type" : "UPDATE_TASK",
                "task_id" : id,
                "updation_dict":json.dumps(updation_dict),
                "metadata":json.dumps(metadata)
            })

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

        rowcount = cursor.rowcount

        if rowcount:
            r.xadd("task_events", {
                "event_type" : "DELETE_TASK",
                "task_id" : task_id,
            })

        return True
    except Exception as e:
        print("Error deleting task : ",e)
        return False
