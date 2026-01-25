import asyncio
from telethon import TelegramClient
from telethon.errors import FloodWaitError
import random

# STRICT RULES (LOCKED)
MIN_GROUP_DELAY = 60      # 60 seconds strict gap between groups
MIN_MESSAGE_DELAY = 20    # 20 seconds min interval for any action
DEFAULT_INTERVAL = 200    # Default loop interval

class Scheduler:
    def __init__(self, session_file, api_id, api_hash, groups, interval_minutes=60):
        self.session_file = session_file
        self.api_id = api_id
        self.api_hash = api_hash
        self.groups = groups          # list of group IDs/Links
        
        # STRICT: Minimum 20 minutes loop interval (1200 seconds)
        # Even if frontend sends less, backend enforces 20m
        sanitized_interval = max(interval_minutes, 20)
        self.interval_seconds = sanitized_interval * 60
        self.running = False
        self.client = None

    async def get_latest_saved_messages(self, limit=5):
        """Fetch latest messages from Saved Messages (me)"""
        msgs = []
        try:
            # Reverse=False gets newest first by default in iter_messages
            # We want to process oldest to newest? Or just cycle newest?
            # Master doc says "Top to bottom (oldest to newest)" logic usually implies
            # reading history. For automation, usually we cycle a set.
            # Let's fetch recent 10 and use them as the "Ad Set"
            async for message in self.client.iter_messages('me', limit=limit):
                if message.text:
                    msgs.append(message.text)
            
            # Reverse to cycle oldest -> newest
            return msgs[::-1] 
        except Exception as e:
            print(f"[ERROR] Fetching Saved Messages: {e}")
            return []

    async def start(self):
        self.running = True
        self.client = TelegramClient(self.session_file, self.api_id, self.api_hash)
        await self.client.connect()

        if not await self.client.is_user_authorized():
            print("[ERROR] Session invalid, stopping scheduler")
            self.running = False
            return

        print(f"[INFO] Scheduler started. Gap: {MIN_GROUP_DELAY}s, Interval: {self.interval_seconds}s")

        try:
            while self.running:
                # 1. Refresh Content from Saved Messages
                messages = await self.get_latest_saved_messages(limit=10)
                
                if not messages:
                    print("[WARN] No messages found in Saved Messages. Waiting...")
                    await asyncio.sleep(60)
                    continue

                print(f"[INFO] Loaded {len(messages)} messages from Saved Messages")

                # 2. Cycle through loaded messages
                for message_text in messages:
                    if not self.running: break

                    # 3. Send to all groups
                    for group in self.groups:
                        if not self.running: break

                        try:
                            print(f"[SENDING] To {group}...")
                            await self.client.send_message(group, message_text)
                            
                            # STRICT RULE: 60s Group Gap
                            print(f"[WAIT] {MIN_GROUP_DELAY}s group gap...")
                            await asyncio.sleep(MIN_GROUP_DELAY)

                        except FloodWaitError as e:
                            print(f"[FLOOD] Waiting {e.seconds}s...")
                            await asyncio.sleep(e.seconds)
                        except Exception as e:
                            print(f"[ERROR] Sending to {group}: {e}")
                            # Still wait to prevent rapid fail loops
                            await asyncio.sleep(MIN_GROUP_DELAY)
                    
                    # Wait 10s between different messages in same loop? 
                    # Or just proceed?
                    await asyncio.sleep(10)

                # 4. Wait for next full interval cycle
                print(f"[CYCLE] Completed. Waiting {self.interval_seconds}s...")
                await asyncio.sleep(self.interval_seconds)

        except Exception as e:
            print(f"[CRITICAL] Scheduler crashed: {e}")
        finally:
            await self.client.disconnect()

    def stop(self):
        self.running = False
