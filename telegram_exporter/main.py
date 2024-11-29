import os
import sqlite3
import re
import logging
import argparse
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from dotenv import load_dotenv
from telethon.tl.types import (
    MessageEntityBold,
    MessageEntityItalic,
    MessageEntityUnderline,
    MessageEntityStrike,
    MessageEntityCode,
    MessageEntityPre,
    MessageEntityUrl,
    MessageEntityTextUrl,
)
from telethon.utils import add_surrogate
from telethon.tl.custom.message import Message

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
PHONE = os.getenv("PHONE")

# Create Telegram client
client = TelegramClient("session_name", API_ID, API_HASH)


def ensure_table_structure(cursor):
    """
    Ensures the 'messages' table has the required columns.
    Adds missing columns if necessary.
    """
    cursor.execute("PRAGMA table_info(messages)")
    existing_columns = {row[1] for row in cursor.fetchall()}

    required_columns = {
        "id": "INTEGER PRIMARY KEY",
        "chat_id": "INTEGER",
        "message_text": "TEXT",
        "date": "TEXT",
        "urls": "TEXT",
    }

    for column_name, column_type in required_columns.items():
        if column_name not in existing_columns:
            logger.info(f"Adding missing column: {column_name}")
            cursor.execute(
                f"ALTER TABLE messages ADD COLUMN {column_name} {column_type}"
            )


def extract_urls_from_message(message: Message) -> list:
    """
    Extracts URLs from the message text and its entities.

    Args:
        message (Message): Telegram message object.

    Returns:
        list: A list of unique URLs.
    """
    urls = []

    # Extract URLs from the plain text of the message
    if message.message:
        text_urls = re.findall(r"https?://[^\s\">]+", message.message)
        urls.extend(text_urls)

    # Extract URLs from entities in the message
    entities = message.entities or []
    for entity in entities:
        if isinstance(entity, MessageEntityUrl):
            offset = entity.offset
            length = entity.length
            entity_text = message.message[offset:offset + length]
            urls.append(entity_text)
        elif isinstance(entity, MessageEntityTextUrl):
            urls.append(entity.url)

    return list(set(urls))  # Remove duplicates


def format_message_to_html(message: Message) -> str:
    """
    Converts a Telegram message into HTML format.

    Args:
        message (Message): Telegram message object.

    Returns:
        str: HTML-formatted message.
    """
    if not message.message:
        return ""

    text = add_surrogate(message.message)
    entities = sorted(message.entities or [], key=lambda e: e.offset)

    result = []
    current_index = 0

    for entity in entities:
        start = entity.offset
        end = start + entity.length
        entity_text = text[start:end]
        result.append(text[current_index:start])

        if isinstance(entity, MessageEntityBold):
            result.append(f"<b>{entity_text}</b>")
        elif isinstance(entity, MessageEntityItalic):
            result.append(f"<i>{entity_text}</i>")
        elif isinstance(entity, MessageEntityUnderline):
            result.append(f"<u>{entity_text}</u>")
        elif isinstance(entity, MessageEntityStrike):
            result.append(f"<s>{entity_text}</s>")
        elif isinstance(entity, MessageEntityCode):
            result.append(f"<code>{entity_text}</code>")
        elif isinstance(entity, MessageEntityPre):
            result.append(f"<pre>{entity_text}</pre>")
        elif isinstance(entity, MessageEntityUrl):
            result.append(f'<a href="{entity_text}">{entity_text}</a>')
        elif isinstance(entity, MessageEntityTextUrl):
            result.append(f'<a href="{entity.url}">{entity_text}</a>')
        else:
            result.append(entity_text)

        current_index = end

    result.append(text[current_index:])
    return "".join(result).encode("utf-16", "surrogatepass").decode("utf-16")


async def main():
    parser = argparse.ArgumentParser(
        description="Export Telegram messages to an SQLite database."
    )
    parser.add_argument(
        "--chat",
        type=str,
        default="me",
        help=(
            "Username, ID, or link of the chat/channel "
            "to export messages from."
        ),
    )
    args = parser.parse_args()

    try:
        # Start Telegram client
        await client.start(PHONE)
        if not await client.is_user_authorized():
            try:
                await client.send_code_request(PHONE)
                await client.sign_in(PHONE, input("Enter the code: "))
            except SessionPasswordNeededError:
                await client.sign_in(password=input("Enter your password: "))

        # Get the target chat
        chat_input = args.chat
        try:
            chat = await client.get_entity(chat_input)
            logger.info(
                "Exporting messages from chat: "
                f"{chat.title if hasattr(chat, 'title') else chat.username}"
            )
        except Exception as e:
            logger.error(f"Failed to get chat '{chat_input}': {e}")
            return

        # Connect to the database and ensure table structure
        db_path = os.path.join("data", "db.sqlite3")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY
            )
            """
        )
        ensure_table_structure(cursor)

        # Fetch messages and save them to the database
        messages = await client.get_messages(chat, limit=None)

        for message in messages:
            if message.message:
                cursor.execute(
                    "SELECT urls FROM messages WHERE id = ?", (message.id,)
                )
                result = cursor.fetchone()

                urls = ", ".join(extract_urls_from_message(message))

                if result:
                    existing_urls = result[0]
                    if urls != existing_urls:
                        cursor.execute(
                            "UPDATE messages SET urls = ? WHERE id = ?",
                            (urls, message.id),
                        )
                        logger.info(f"Updated URLs for message {message.id}")
                    else:
                        logger.info(
                            f"Message {message.id} already exists, skipping."
                        )
                else:
                    formatted_message = format_message_to_html(message)
                    cursor.execute(
                        """
                        INSERT INTO messages
                        (id, chat_id, message_text, date, urls)
                        VALUES (?, ?, ?, ?, ?)
                        """,
                        (
                            message.id,
                            message.chat_id,
                            formatted_message,
                            str(message.date),
                            urls,
                        ),
                    )
                    logger.info(
                        f"Inserted new message {message.id} into the database."
                    )

        conn.commit()
        conn.close()
        logger.info("Messages have been successfully exported to the database")

    except Exception as e:
        logger.error(f"An error occurred: {e}")


if __name__ == "__main__":
    with client:
        client.loop.run_until_complete(main())
