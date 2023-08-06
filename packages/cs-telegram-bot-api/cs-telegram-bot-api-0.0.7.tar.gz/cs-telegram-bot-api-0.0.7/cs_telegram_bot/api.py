"""
A Python module for interacting with the Telegram Bot API.
"""
import requests
import os
import logging
from secrets_loader import load_secret


class TelegramClient:
    """
    A client for the Telegram Bot API.
    """

    def __init__(self, bot_token=None):
        """
        Create a new TelegramClient.
        """
        self.bot_token = bot_token or load_secret("TELEGRAM_TOKEN")
        self.offset = 0

    def get_new_messages(self):
        """
        Get new messages from the API.
        """
        try:
            response = requests.get(
                f"https://api.telegram.org/bot{self.bot_token}/getUpdates",
                params={
                    "offset": self.offset  # Only get updates with higher offsets
                }
            )
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)

        result = response.json()["result"]

        # Get the messages from the updates
        messages = []
        for update in result:
            if "message" in update:
                messages.append(update["message"])

        # Update the offset
        if result:
            self.offset = result[-1]["update_id"] + 1

        return messages

    def send_message(self, chat_id, message):
        """
        Send a message to a chat.
        """
        try:
            response = requests.post(
                "https://api.telegram.org/bot{}/sendMessage".format(
                    self.bot_token),
                json={
                    "chat_id": chat_id,
                    "text": message
                }
            )
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)

        # If the API call was successful, the response will contain
        # the sent message in the "result" field
        result = response.json()["result"]
        logging.info(message.encode())
        return result

