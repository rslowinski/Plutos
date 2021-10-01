import json

from telethon import TelegramClient, events
from TTypes import RawTMessage
from TelegramCallsHandler import TelegramCallsHandler

credentials_path = 'k_credentials.json'

with open(credentials_path) as f:
    credentials = json.load(f)

api_id = credentials['id']
api_hash = credentials['hash']

client = TelegramClient(credentials_path, api_id, api_hash)
client.start()

allowed_chats = ['ACP: Walsh Wealth Group']
all_events = []

allowed_message_triggers = ['🚀trades'] #['johnny', 'trades', 'Astekz', 'cryptoEliZ']

calls_handler = TelegramCallsHandler()

def message_filter(mssg):
    for trigger in allowed_message_triggers:
        if trigger in mssg:
            return True
    return False


@client.on(events.NewMessage(incoming=True, chats=allowed_chats, pattern=message_filter))
async def handler(e):
    print(f"\nNew message={e.message}")
    calls_handler.add_msgs([RawTMessage(e.message.message, e.date)])


with client:
    client.run_until_disconnected()