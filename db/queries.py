from db.connection import conn, cursor

#-------------------------------INSERT TASK------------------------------------------
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
        print("insert task : task id :",task_id)

        conn.commit()

        return task_id
    except Exception as e:
        print("Error inserting task : ",e)
#------------------------------------------------------------------------------------

#-------------------------------UPDATE TASK------------------------------------------
def update_task(updation_dict_list : list):
    total_updated = 0
    updated_ids = []
    try:
        # buildint SET clause
        print("updation_dict_list : ", updation_dict_list)

        for updation_dict in updation_dict_list:
            id = updation_dict['id']
            updation_dict.pop('id', None)

            set_clause = ", ".join([f"{key} = %s" for key in updation_dict.keys()])

            final_query = f"UPDATE tasks SET {set_clause} WHERE id = %s"

            values = list(updation_dict.values()) + [int(id)]

            print("Updated query  :",final_query)
            print("Values :", values)
            cursor.execute(final_query, values)
            total_updated += cursor.rowcount

            if cursor.rowcount:
                updated_ids.append(id)

        conn.commit()

        return {
            'success':True,
            'updated_ids':updated_ids,
            'update_count':total_updated,
            'error':None
        }

    except Exception as e:
        print("Error updating task : ",e)
        return {
            'success':False,
            'updated_ids':updated_ids,
            'update_count':total_updated,
            'error':str(e)
        }
#------------------------------------------------------------------------------------

#-------------------------------DELETE TASK------------------------------------------
def delete_task(task_ids : list):
    try:
        if not task_ids:
            return False
        
        placeholders = ','.join(['%s'] * len(task_ids))

        cursor.execute(f"""
        DELETE FROM tasks where id IN ({placeholders})
        """, task_ids)

        conn.commit()

        rowcount = cursor.rowcount

        if not rowcount:
            return False

        return True
    except Exception as e:
        print("Error deleting task : ",e)
        return False
#------------------------------------------------------------------------------------

#-------------------------------FETCH ALL TASKS--------------------------------------
def fetch_all_tasks():
    try:
        cursor.execute("""
        SELECT * FROM tasks
        """)

        tasks = cursor.fetchall()

        return tasks

    except Exception as e:
        print("Error fetching tasks : ",e)
        return False
#------------------------------------------------------------------------------------

#-------------------------------FETCH SPECIFIC TASKS--------------------------------------
def fetch_specific_tasks(ids:list):
    try:
        if not ids:
            return False
        
        placeholders = ','.join(['%s'] * len(ids))

        cursor.execute(f"""
        SELECT * FROM tasks WHERE id IN({placeholders})
        """,ids)

        tasks = cursor.fetchall()

        return tasks

    except Exception as e:
        print("Error fetching specific tasks : ",e)
        return False
#------------------------------------------------------------------------------------

#-------------------------------INSERT TASK------------------------------------------
def insert_draft(draft : dict):
    try:
        cursor.execute("""
        INSERT INTO drafts(title, text)
        VALUES(%s, %s)
        """,(
            draft['title'],
            draft['text'],
        ))

        draft_id = cursor.lastrowid
        print("insert draft : draft id :",draft_id)

        conn.commit()

        return cursor.rowcount
    except Exception as e:
        print("Error inserting draft : ",e)
        return cursor.rowcount
#------------------------------------------------------------------------------------