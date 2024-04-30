import threading
import json

lock = threading.Lock()

def manage_chat_history(uuid, update=None):
    with lock:
        try:
            with open('chat_history.json', 'r') as file:
                chat_history = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            chat_history = {}
        
        if update:
            if uuid in chat_history:
                chat_history[uuid].append(update)
            else:
                chat_history[uuid] = [update]
        
            with open('chat_history.json', 'w') as file:
                json.dump(chat_history, file, indent=4)
        
        return chat_history.get(uuid, [])
