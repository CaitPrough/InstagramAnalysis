import os
import json
from collections import defaultdict
import datetime

root_folder = 'C:\\Users\\caitp\\OneDrive\\Desktop\\Insta\\inbox'

message_counts = defaultdict(lambda: defaultdict(int))
hourly_message_counts = defaultdict(lambda: defaultdict(int))

def process_message(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data_file = json.load(file)
    
    participants = sorted(participant['name'] for participant in data_file['participants'])
    chat_key = tuple(participants)
    
    for message in data_file['messages']:
        sender_name = message['sender_name']
        
        # messages
        message_counts[chat_key][sender_name] += 1
        
        # extract hour from timestamp
        timestamp_ms = message['timestamp_ms']
        dt = datetime.datetime.fromtimestamp(timestamp_ms / 1000.0)
        hour = dt.hour
        hourly_message_counts[chat_key][hour] += 1

def print_summary():
    for chat_key in sorted(message_counts):
        total_messages = sum(message_counts[chat_key].values())
        
        participant_names_str = ', '.join(chat_key)
        print(f"Chat Participants: {participant_names_str}")
        
        for participant in sorted(message_counts[chat_key]):
            message_count = message_counts[chat_key][participant]
            percentage = (message_count / total_messages) * 100
            print(f"{participant} - {percentage:.2f}% - {message_count}")
        
        print("Hourly Message Counts:")
        for hour in range(24):
            if total_messages > 0:
                hour_percentage = (hourly_message_counts[chat_key][hour] / total_messages) * 100
            else:
                hour_percentage = 0.0
            print(f"{hour:02}: {hour_percentage:.2f}% - {hourly_message_counts[chat_key][hour]}")
        
        print()

def process_messages():
    for folder_path, _, files in os.walk(root_folder):
        for filename in files:
            if filename.startswith("message_") and filename.endswith(".json"):
                file_path = os.path.join(folder_path, filename)
                process_message(file_path)

process_messages()
print_summary()
