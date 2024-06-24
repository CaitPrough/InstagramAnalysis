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

    # Sort messages by timestamp
    messages.sort(key=lambda x: x['timestamp_ms'])

    # Initialize dictionaries to store time differences
    time_diffs = defaultdict(lambda: defaultdict(list))

    # Iterate through sorted messages to calculate time differences
    for i in range(1, len(messages)):
        sender_name = messages[i]['sender_name']
        prev_sender_name = messages[i-1]['sender_name']
        timestamp1 = convert_timestamp(messages[i-1]['timestamp_ms'])
        timestamp2 = convert_timestamp(messages[i]['timestamp_ms'])
        time_diff = timestamp2 - timestamp1

        # Store time difference
        time_diffs[chat_key][sender_name].append(time_diff)

    # Calculate average and longest time between messages
    avg_times = {}
    longest_times = {}
    for participant in participants:
        if participant in time_diffs[chat_key]:
            diffs = time_diffs[chat_key][participant]
            if diffs:
                avg_time = sum(diffs, timedelta()) / len(diffs)
                longest_time = max(diffs)
                avg_times[participant] = avg_time
                longest_times[participant] = longest_time

    # Print results for each conversation
    print(f"CHAT PARTICIPANTS: {', '.join(participants)}")
    for participant in participants:
        avg_time_str = str(avg_times.get(participant, timedelta(seconds=0)))
        longest_time_str = str(longest_times.get(participant, timedelta(seconds=0)))
        print(f"{participant}: Average time between messages: {avg_time_str}, Longest time between messages: {longest_time_str}")
    print("-" * 30)

def process_messages():
    for folder_path, _, files in os.walk(root_folder):
        for filename in files:
            if filename.startswith("message_") and filename.endswith(".json"):
                file_path = os.path.join(folder_path, filename)
                process_message(file_path)

process_messages()
