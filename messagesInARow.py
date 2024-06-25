import os
import json
from collections import defaultdict

# Define the root directory containing user folders
root_folder = 'C:\\Users\\caitp\\OneDrive\\Desktop\\Insta\\inbox'

consecutive_message_counts = defaultdict(lambda: defaultdict(list))
consecutive_messages = defaultdict(lambda: defaultdict(list))

def count_consecutive_messages(data_file):
    participants = sorted(participant['name'] for participant in data_file['participants'])
    chat_key = tuple(participants)
    current_sender = None
    current_count = 0
    current_messages = []
    
    for message in data_file['messages']:
        sender_name = message['sender_name']
        
        # Skip reactions
        if 'reactions' in message:
            continue
        
        if sender_name != current_sender:
            if current_sender is not None:
                consecutive_message_counts[chat_key][current_sender].append(current_count)
                consecutive_messages[chat_key][current_sender].append(current_messages)
            current_sender = sender_name
            current_count = 1
            current_messages = [message]
        else:
            current_count += 1
            current_messages.append(message)
    
    # Update for the last sender in the chat
    if current_sender is not None:
        consecutive_message_counts[chat_key][current_sender].append(current_count)
        consecutive_messages[chat_key][current_sender].append(current_messages)

def calculate_stats():
    stats = defaultdict(lambda: defaultdict(dict))
    for chat_key, participants in consecutive_message_counts.items():
        for participant, counts in participants.items():
            if counts:
                avg_count = sum(counts) / len(counts)
                max_count = max(counts)
                max_index = counts.index(max_count)
                max_messages = consecutive_messages[chat_key][participant][max_index]
                stats[chat_key][participant]['average'] = avg_count
                stats[chat_key][participant]['max'] = max_count
                stats[chat_key][participant]['max_messages'] = max_messages
    return stats

def process_message(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data_file = json.load(file)
    
    count_consecutive_messages(data_file)

def process_messages_in_folder(folder_path):
    for filename in os.listdir(folder_path):
        if filename.startswith("message_") and filename.endswith(".json"):
            file_path = os.path.join(folder_path, filename)
            process_message(file_path)

def get_consecutive_stats():
    stats_output = ""
    stats = calculate_stats()
    for chat_key in sorted(stats):
        participant_names_str = ', '.join(chat_key)
        stats_output += f"CHAT PARTICIPANTS: {participant_names_str}\n"
        
        for participant in sorted(stats[chat_key]):
            avg_count = stats[chat_key][participant]['average']
            max_count = stats[chat_key][participant]['max']
            max_messages = stats[chat_key][participant]['max_messages']
            stats_output += f"{participant}:\n"
            stats_output += f"  Average: {avg_count:.2f}\n"
            stats_output += f"  Max: {max_count}\n"
            stats_output += f"  Messages in a row:\n"
            for message in max_messages:
                if isinstance(message, list):  # Check if it's a list of messages
                    for msg in message:
                        stats_output += f"    {msg.get('content', '[Attachment or other type of message]')}\n"
                else:  # Single message case
                    stats_output += f"    {message.get('content', '[Attachment or other type of message]')}\n"
        stats_output += "-\n"
    
    return stats_output

