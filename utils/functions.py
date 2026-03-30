import dateparser
from langchain_core.documents import Document

def due_time_parser(date_str):

    parsed_date = dateparser.parse(
        date_str, 
        settings={"TIMEZONE": "Asia/Karachi", "RETURN_AS_TIMEZONE_AWARE": True}
    )

    if parsed_date is None:
        return None
    else:
        return parsed_date.isoformat()


# Function for making document objs of task
def make_doc(task, id):
    page_content = f"""Task title is {task['title']}, task description is {task['description']}, task category is {task['category']}, task priority is {task['priority']}, task due time is {str(task['due_time'])}
    """
    metadata = task.copy()
    metadata['task_id'] = id
    return Document(
        page_content = page_content,
        metadata = metadata
    )

def make_updated_doc(updation_dict, old_task):
    updated_task = old_task.copy()

    for key, value in updation_dict.items():
        updated_task[key] = value

    page_content = f"""Task title is {updated_task.get('title', '')}, task description is {updated_task.get('description', '')}, task category is {updated_task.get('category', '')}, task priority is {updated_task.get('priority', '')}, task due time is {str(updated_task.get('due_time', ''))}.
    """

    return Document(
        page_content = page_content,
        metadata = updated_task
    )
