import os
import json
import string
from collections import defaultdict
from operator import itemgetter

root_folder = 'C:\\Users\\caitp\\OneDrive\\Desktop\\Insta\\inbox'

def process_messages(file_path, word_counts):
    with open(file_path, 'r', encoding='utf-8') as file:
        data_file = json.load(file)
    
    participants = sorted(participant['name'] for participant in data_file['participants'])
    chat_key = tuple(participants)
    
    for message in data_file['messages']:
        if 'share' in message:
            continue
        
        sender_name = message['sender_name']
        
        if 'content' not in message:
            continue
        
        content = message['content'] 
        
        if sender_name in participants:
            words = content.split()
            
            for word in words:
                cleaned_word = word.strip(string.punctuation).lower()
                
                if cleaned_word.isalpha() and len(cleaned_word) > 1:
                    word_counts[chat_key][cleaned_word] += 1

def analyze_conversations():
    word_counts = defaultdict(lambda: defaultdict(int))
    
    for folder_path, _, files in os.walk(root_folder):
        for filename in files:
            if filename.startswith("message_") and filename.endswith(".json"):
                file_path = os.path.join(folder_path, filename)
                process_messages(file_path, word_counts)
    
    for chat_key, chat_word_counts in word_counts.items():
        participant_names_str = ', '.join(chat_key)
        print(f"Chat Participants: {participant_names_str}")
        
        popular_words = {word: count for word, count in chat_word_counts.items() if count > 10}
        
        sorted_words = sorted(popular_words.items(), key=itemgetter(1), reverse=True)
        
        for word, count in sorted_words:
            print(f"{word}: {count}")
        
        print()  
        
analyze_conversations()
