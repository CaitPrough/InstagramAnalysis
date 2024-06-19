import os
import json
from collections import defaultdict

root_folder = 'C:\\Users\\caitp\\OneDrive\\Desktop\\Insta\\inbox'

message_counts = defaultdict(lambda: defaultdict(int))
reaction_counts = defaultdict(lambda: defaultdict(int))
attachment_counts = defaultdict(lambda: defaultdict(int))

def process_message(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data_file = json.load(file)
    
    participants = sorted(participant['name'] for participant in data_file['participants'])
    chat_key = tuple(participants)
    
    for message in data_file['messages']:
        sender_name = message['sender_name']
        
        # messages
        message_counts[chat_key][sender_name] += 1
        
        # reactions
        if 'reactions' in message:
            for reaction in message['reactions']:
                actor = reaction['actor']
                reaction_counts[chat_key][actor] += 1

        # attachments
        if 'share' in message:
            attachment_counts[chat_key][sender_name] += 1

def print_summary():
    for chat_key in sorted(message_counts):
        participant_names_str = ', '.join(chat_key)
        print(f"CHAT PARTICIPANTS: {participant_names_str}")
        
        for participant in sorted(message_counts[chat_key]):
            message_count = message_counts[chat_key][participant]
            print(f"{participant} sent {message_count} messages.")
        print("-")    
        
        for participant in sorted(reaction_counts[chat_key]):
            reaction_count = reaction_counts[chat_key][participant]
            print(f"{participant} reacted {reaction_count} times.")
        print("-")
        
        for participant in sorted(attachment_counts[chat_key]):
            attachment_count = attachment_counts[chat_key][participant]
            print(f"{participant} sent {attachment_count} attachments.")
        print()
        print()

def process_messages():
    for folder_path, _, files in os.walk(root_folder):
        for filename in files:
            if filename.startswith("message_") and filename.endswith(".json"):
                file_path = os.path.join(folder_path, filename)
                process_message(file_path)

process_messages()
print_summary()
