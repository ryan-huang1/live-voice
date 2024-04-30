import threading
import json

lock = threading.Lock()

def manage_chat_history(uuid, text):
    with lock:
        try:
            with open('chat_history.json', 'r') as file:
                chat_history = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            chat_history = {}
        
        if uuid in chat_history:
            chat_history[uuid].append(text)
        else:
            chat_history[uuid] = [text]
        
        with open('chat_history.json', 'w') as file:
            json.dump(chat_history, file, indent=4)