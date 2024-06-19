import os
import json
from collections import defaultdict

root_folder = 'inbox'

participant_groups = defaultdict(lambda: defaultdict(int))

def message_count(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data_file = json.load(file)
    
    participant_names = sorted(participant['name'] for participant in data_file['participants'])
    group_key = tuple(participant_names)
    
    for message in data_file['messages']:
        sender_name = message['sender_name']
        participant_groups[group_key][sender_name] += 1

for folder_path, _, files in os.walk(root_folder):
    for filename in files:
        if filename.startswith("message_") and filename.endswith(".json"):
            file_path = os.path.join(folder_path, filename)
            
            message_count(file_path)

for group_key, group_counts in participant_groups.items():
    participant_names_str = ', '.join(group_key)
    print(f"Message Participants: {participant_names_str}")
    for participant, count in group_counts.items():
        print(f"{participant} sent {count} messages.")
    print() 
