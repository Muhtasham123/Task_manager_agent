from states.tm_state import TaskManagerState
import dateparser

def dates_parser(state : TaskManagerState):
    task = state['task']
    date_str = task['due_time']
    
    if not date_str or str(date_str).lower() == "null":
        return {
        'task':task
    }

    parsed_date = dateparser.parse(
        date_str, 
        settings={"TIMEZONE": "Asia/Karachi", "RETURN_AS_TIMEZONE_AWARE": True}
    )

    if parsed_date is None:
        task['due_time'] = "null"
    else:
        task['due_time'] = parsed_date.isoformat()

    return {
        'task':task
    }
