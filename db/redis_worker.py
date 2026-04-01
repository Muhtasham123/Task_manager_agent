from db.connection import r, cursor
from db.vector_store import vec_store
from utils.functions import make_doc, make_updated_doc
import json

STREAM = "task_events"
CONSUMER_GROUP = "task_events_group"
CONSUMER_NAME = "C_1"

# Creating consumer group
try:
    r.xgroup_create(STREAM, CONSUMER_GROUP, "0", mkstream=True)
except Exception as e:
    print("Consumer group already exists or error:", e)


# Event processing function
def process_event(event_data, event_id):
    
    try:
        event_type = event_data.get('event_type')
        task_id = event_data.get('task_id')

        if not task_id:
            r.xack(STREAM, CONSUMER_GROUP, event_id)
            return 
        task_id = str(task_id)

        task = None
        #fetching task from database
        if event_type in ("CREATE_TASK", "UPDATE_TASK"):
            cursor.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
            task = cursor.fetchone()

        

        if event_type == "CREATE_TASK":
            if not task:
                r.xack(STREAM, CONSUMER_GROUP, event_id)
                return 

            task_doc = make_doc(task, task_id)
            #adding task in vector store 
            vec_store.add_documents(documents=[task_doc], ids = [str(task_id)])

        elif event_type == "UPDATE_TASK":
            if not task:
                r.xack(STREAM, CONSUMER_GROUP, event_id)
                return 

            updation_dict = json.loads(event_data.get('updation_dict', '{}'))
            metadata = json.loads(event_data.get('metadata', '{}'))
            updated_doc = make_updated_doc(updation_dict, metadata)

            #updating in vector store
            vec_store.update_document(document_id = task_id, document=updated_doc)

        elif event_type == "DELETE_TASK":
            # deleting task from vector store as well
            vec_store.delete(ids = [str(task_id)])

        r.xack(STREAM, CONSUMER_GROUP, event_id)

    except Exception as e:
        print("Error processing event : ", e)


#Retry pending events using AUTOCLAIM
def retry_pending():
    next_id = "0-0"

    while True:
        result = r.xautoclaim(
            STREAM,
            CONSUMER_GROUP,
            CONSUMER_NAME,
            10000,
            start_id = next_id
        )

        next_id = result[0]
        events = result[1]

        if not events:
            break

        for event in events:
            event_id, event_data = event
            process_event(event_data, event_id)


#Reading stream for events

def read_stream():

    events = r.xreadgroup(
        streams = {STREAM : ">"},
        consumername = CONSUMER_NAME,
        groupname = CONSUMER_GROUP,
        count = 1,
        block=5000
    )

    if not events:
        return None

    for stream, messages in events:
        for event_id, event_data in messages:
            process_event(event_data, event_id)


#main driver
def main():
    while True:
        retry_pending()
        read_stream()


main()