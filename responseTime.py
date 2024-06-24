import os
import json
from datetime import datetime, timedelta
from collections import defaultdict

root_folder = 'C:\\Users\\caitp\\OneDrive\\Desktop\\Insta\\inbox'

def convert_timestamp(timestamp_ms):
    return datetime.fromtimestamp(timestamp_ms / 1000.0)

def process_message(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data_file = json.load(file)
    
    messages = data_file['messages']
    participants = {p['name'] for p in data_file['participants']}
    chat_key = tuple(sorted(participants))

    messages.sort(key=lambda x: x['timestamp_ms'])

    for i in range(1, len(messages)):
        sender_name = messages[i]['sender_name']
        prev_sender_name = messages[i-1]['sender_name']
        timestamp1 = convert_timestamp(messages[i-1]['timestamp_ms'])
        timestamp2 = convert_timestamp(messages[i]['timestamp_ms'])
        time_diff = timestamp2 - timestamp1
        
        print(f"{prev_sender_name} -> {sender_name}: {time_diff}")

def process_messages():
    for folder_path, _, files in os.walk(root_folder):
        for filename in files:
            if filename.startswith("message_") and filename.endswith(".json"):
                file_path = os.path.join(folder_path, filename)
                process_message(file_path)

process_messages()
