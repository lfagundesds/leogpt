import json
from leogpt.utils import as_json, send_pushover_notification

specs_dir = 'specs'

record_user_details_json = as_json(f'{specs_dir}/record_user_details.json')
record_unknown_question_json = as_json(f'{specs_dir}/record_unknown_question.json')

tools = [{"type": "function", "function": record_user_details_json},
        {"type": "function", "function": record_unknown_question_json}]

def record_user_details(email, name="Name not provided", notes="not provided"):
    send_pushover_notification(f"Recording {name} with email {email} and notes {notes}")
    return {"recorded": "ok"}

def record_unknown_question(question):
    send_pushover_notification(f"Recording {question}")
    return {"recorded": "ok"}

def handle_tool_call(tool_calls):
    results = []
    for tool_call in tool_calls:
        tool_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)
        print(f"Tool called: {tool_name}", flush=True)
        tool = globals().get(tool_name)
        result = tool(**arguments) if tool else {}
        results.append({"role": "tool","content": json.dumps(result),"tool_call_id": tool_call.id})
    return results