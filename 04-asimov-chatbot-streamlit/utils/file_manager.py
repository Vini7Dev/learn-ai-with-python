import re
import pickle
from pathlib import Path

from unidecode import unidecode

CONFIGS_FOLDER = Path(__file__).parent / '..' / 'configs'
CONFIGS_FOLDER.mkdir(exist_ok=True)
MESSAGES_FOLDER = Path(__file__).parent / '..' / 'messages'
MESSAGES_FOLDER.mkdir(exist_ok=True)
CACHE_MESSAGE_NAMES={}

def save_api_key(api_key):
    with open(CONFIGS_FOLDER / 'api_key', 'wb') as f:
        pickle.dump(api_key, f)

def read_api_key():
    if (CONFIGS_FOLDER / 'api_key').exists():
        with open(CONFIGS_FOLDER / 'api_key', 'rb') as f:
            return pickle.load(f)
    else:
        return ''

def convert_file_name(file_name):
    return re.sub('\W+', '', unidecode(file_name)).lower()

def unconvert_file_name(file_name):
    if file_name not in CACHE_MESSAGE_NAMES:
        message_name = load_messages_name_by_file(file_name, key='message_name')
        CACHE_MESSAGE_NAMES[file_name] = message_name
        return message_name
    return CACHE_MESSAGE_NAMES[file_name]

def get_message_name(messages):
    for message in messages:
        if (message['role'] == 'user'):
            return message['content'][:30]

def save_messages(messages):
    if len(messages) == 0:
        return False

    messaage_name = get_message_name(messages=messages)
    file_name = convert_file_name(messaage_name)
    file_to_save = {
        'message_name': messaage_name,
        'file_name': file_name,
        'messages': messages,
    }
    with open(MESSAGES_FOLDER / file_name, 'wb') as f:
        pickle.dump(file_to_save, f)

def load_messages(messages, key='messages'):
    if len(messages) == 0:
        return []

    messaage_name = get_message_name(messages=messages)
    file_name = convert_file_name(messaage_name)
    with open(MESSAGES_FOLDER / file_name, 'rb') as f:
        messages = pickle.load(f)
    return messages[key]

def load_messages_name_by_file(file_name, key='messages'):
    with open(MESSAGES_FOLDER / file_name, 'rb') as f:
        messages = pickle.load(f)
    return messages[key]
