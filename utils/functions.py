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
