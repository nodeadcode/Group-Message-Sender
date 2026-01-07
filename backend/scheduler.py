import asyncio
from telethon import TelegramClient
from telethon.errors import FloodWaitError

# Fixed delays (LOCKED)
GROUP_DELAY = 15      # seconds
MESSAGE_DELAY = 200   # seconds


class Scheduler:
    def __init__(self, session_file, api_id, api_hash, groups, messages):
        self.session_file = session_file
        self.api_id = api_id
        self.api_hash = api_hash
        self.groups = groups          # list of group IDs
        self.messages = messages      # list of ad messages
        self.running = False

    async def start(self):
        self.running = True
        client = TelegramClient(self.session_file, self.api_id, self.api_hash)
        await client.connect()

        try:
            while self.running:
                for message in self.messages:
                    if not self.running:
                        break

                    for group in self.groups:
                        if not self.running:
                            break

                        try:
                            await client.send_message(group, message)
                            await asyncio.sleep(GROUP_DELAY)

                        except FloodWaitError as e:
                            # Telegram asked to wait
                            await asyncio.sleep(e.seconds)

                        except Exception as e:
                            print(f"[ERROR] {group}: {e}")

                    # wait before next message
                    await asyncio.sleep(MESSAGE_DELAY)

        finally:
            await client.disconnect()

    def stop(self):
        self.running = False
