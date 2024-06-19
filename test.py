import os
import json
from collections import defaultdict

# Specify the root folder containing nested 'inbox' structure
root_folder = 'inbox'

# Dictionary to accumulate message counts for each participant
message_counts = defaultdict(int)

# Function to process JSON files
def process_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data_file = json.load(file)
    
    # Count messages for each sender in the current JSON file
    for message in data_file['messages']:
        sender_name = message['sender_name']
        message_counts[sender_name] += 1

# Walk through all folders and subfolders
for folder_path, _, files in os.walk(root_folder):
    for filename in files:
        if filename.startswith("message_") and filename.endswith(".json"):
            file_path = os.path.join(folder_path, filename)
            
            # Process the JSON file
            print(f"Processing file: {file_path}")
            process_json_file(file_path)

# Print message counts for each participant after processing all files
for participant, count in message_counts.items():
    print(f"{participant} sent {count} messages.")
