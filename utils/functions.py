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
    task_clean = task.copy()
    task_clean['due_time'] = str(task_clean['due_time'])
    task_clean['created_at'] = str(task_clean['created_at'])

    page_content = f"""Task title is {task_clean['title']}, task description is {task_clean['description']}, task category is {task_clean['category']}, task priority is {task_clean['priority']}, task due time is {task_clean['due_time']}
    """

    metadata = task_clean

    return Document(
        ids = [id],
        page_content = page_content,
        metadata = metadata
    )

def make_updated_doc(updation_dict, old_task):
    updated_task_clean = old_task.copy()
    updated_task_clean['due_time'] = str(updated_task_clean['due_time'])
    updated_task_clean['created_at'] = str(updated_task_clean['created_at'])

    for key, value in updation_dict.items():
        updated_task_clean[key] = value

    page_content = f"""Task title is {updated_task_clean.get('title', '')}, task description is {updated_task_clean.get('description', '')}, task category is {updated_task_clean.get('category', '')}, task priority is {updated_task_clean.get('priority', '')}, task due time is {str(updated_task_clean.get('due_time', ''))}.
    """

    return Document(
        page_content = page_content,
        metadata = updated_task_clean
    )
