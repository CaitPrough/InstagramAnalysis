import os
import json
from collections import defaultdict
import datetime

root_folder = 'C:\\Users\\caitp\\OneDrive\\Desktop\\Insta\\inbox'

message_counts = defaultdict(lambda: defaultdict(int))
daily_message_counts = defaultdict(lambda: defaultdict(int))

def process_message(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data_file = json.load(file)
    
    participants = sorted(participant['name'] for participant in data_file['participants'])
    chat_key = tuple(participants)
    
    for message in data_file['messages']:
        sender_name = message['sender_name']
        
        # messages
        message_counts[chat_key][sender_name] += 1
        
        # extract day of the week from timestamp (0 = Monday, ..., 6 = Sunday)
        timestamp_ms = message['timestamp_ms']
        dt = datetime.datetime.fromtimestamp(timestamp_ms / 1000.0)
        day_of_week = dt.weekday()  # Monday is 0 and Sunday is 6
        daily_message_counts[chat_key][day_of_week] += 1

def print_summary():
    for chat_key in sorted(message_counts):
        total_messages = sum(message_counts[chat_key].values())
        
        participant_names_str = ', '.join(chat_key)
        print(f"Chat Participants: {participant_names_str}")
        
        for participant in sorted(message_counts[chat_key]):
            message_count = message_counts[chat_key][participant]
            percentage = (message_count / total_messages) * 100
            print(f"{participant} - {percentage:.2f}% - {message_count}")
        
        print("Daily Message Counts:")
        days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        for day in range(7):
            if total_messages > 0:
                day_percentage = (daily_message_counts[chat_key][day] / total_messages) * 100
            else:
                day_percentage = 0.0
            print(f"{days_of_week[day]} - {day_percentage:.2f}% - {daily_message_counts[chat_key][day]}")
        
        print()

def process_messages():
    for folder_path, _, files in os.walk(root_folder):
        for filename in files:
            if filename.startswith("message_") and filename.endswith(".json"):
                file_path = os.path.join(folder_path, filename)
                process_message(file_path)

process_messages()
print_summary()
