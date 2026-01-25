from telethon import events
import asyncio
import random
from datetime import datetime
from models import AutoReplySettings
import logging

logger = logging.getLogger(__name__)

class AutoReplyHandler:
    """
    Handles auto-reply functionality for Telegram accounts.
    Auto-replies to incoming personal messages based on user settings.
    """
    
    def __init__(self, client, account_id, db_session):
        self.client = client
        self.account_id = account_id
        self.db = db_session
        self.settings = None
        self.handler = None
    
    async def load_settings(self):
        """Load auto-reply settings from database"""
        self.settings = self.db.query(AutoReplySettings).filter(
            AutoReplySettings.account_id == self.account_id
        ).first()
        
        if not self.settings:
            # Create default settings if none exist
            self.settings = AutoReplySettings(
                account_id=self.account_id,
                is_enabled=False,
                reply_messages=["Thanks for your message! I'll get back to you soon."],
                delay_seconds=3,
                use_random_message=False,
                excluded_users=[]
            )
            self.db.add(self.settings)
            self.db.commit()
        
        return self.settings
    
    async def setup(self):
        """Setup the auto-reply event handler"""
        await self.load_settings()
        
        @self.client.on(events.NewMessage(incoming=True))
        async def handle_incoming_message(event):
            try:
                # Check if auto-reply is enabled
                if not self.settings.is_enabled:
                    return
                
                # Only reply to personal messages, not groups/channels
                if event.is_group or event.is_channel:
                    return
                
                # Check if sender is in excluded list
                sender_id = event.sender_id
                if sender_id in self.settings.excluded_users:
                    logger.info(f"Skipping auto-reply for excluded user: {sender_id}")
                    return
                
                # Add random delay (appear human)
                delay = random.randint(
                    max(self.settings.delay_seconds - 1, 2),
                    min(self.settings.delay_seconds + 1, 5)
                )
                logger.info(f"Waiting {delay}s before auto-reply...")
                await asyncio.sleep(delay)
                
                # Select reply message
                if self.settings.use_random_message and len(self.settings.reply_messages) > 1:
                    reply_template = random.choice(self.settings.reply_messages)
                else:
                    reply_template = self.settings.reply_messages[0]
                
                # Get sender info for personalization
                sender = await event.get_sender()
                sender_name = sender.first_name or "there"
                
                # Replace variables in template
                reply = reply_template
                reply = reply.replace("{name}", sender_name)
                reply = reply.replace("{time}", datetime.now().strftime("%H:%M"))
                reply = reply.replace("{date}", datetime.now().strftime("%Y-%m-%d"))
                
                # Send reply
                await event.respond(reply)
                logger.info(f"Auto-reply sent to {sender_name} ({sender_id})")
                
            except Exception as e:
                logger.error(f"Error in auto-reply handler: {e}")
        
        self.handler = handle_incoming_message
        logger.info(f"Auto-reply handler setup for account {self.account_id}")
    
    async def update_settings(self, new_settings):
        """Update auto-reply settings"""
        self.settings.is_enabled = new_settings.get("is_enabled", self.settings.is_enabled)
        self.settings.reply_messages = new_settings.get("reply_messages", self.settings.reply_messages)
        self.settings.delay_seconds = new_settings.get("delay_seconds", self.settings.delay_seconds)
        self.settings.use_random_message = new_settings.get("use_random_message", self.settings.use_random_message)
        self.settings.excluded_users = new_settings.get("excluded_users", self.settings.excluded_users)
        
        self.db.commit()
        logger.info(f"Auto-reply settings updated for account {self.account_id}")
    
    async def toggle(self, enabled: bool):
        """Enable or disable auto-reply"""
        self.settings.is_enabled = enabled
        self.db.commit()
        logger.info(f"Auto-reply {'enabled' if enabled else 'disabled'} for account {self.account_id}")
    
    def remove(self):
        """Remove the event handler"""
        if self.handler and self.client:
            self.client.remove_event_handler(self.handler)
            logger.info(f"Auto-reply handler removed for account {self.account_id}")
