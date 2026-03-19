from states.tm_state import TaskManagerState

# Routing to specific node based on user intent
def intent_router(state : TaskManagerState):
   intent = state['intent']
   if intent == 'create_task':
        return 'create_task'    
   elif intent == 'update_task':
        return 'update_task'
   elif intent == 'delete_task':
        return 'delete_task'
   else:
        return 'other'

# Routing to specific node based on task evaluation status
def eval_router(state : TaskManagerState):
       status = state['task_status']
       iterations = state['iterations']
       max_iterations = state['max_iterations']

       if status == 'optimized' or iterations >= max_iterations:
            return 'complete'
       else:
            return 'needs_optimization'