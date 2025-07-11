import os
import json
from datetime import datetime
from telethon.sync import TelegramClient
from telethon.tl.types import MessageMediaPhoto
from dotenv import load_dotenv

load_dotenv()
api_id = int(os.getenv("TELEGRAM_API_ID"))
api_hash = os.getenv("TELEGRAM_API_HASH")


# You can use your own session name
client = TelegramClient("scraper_session", api_id, api_hash)

# Channels to scrape

channels = [
    "https://t.me/lobelia4cosmetics",
    "https://t.me/tikvahpharma",
    "https://t.me/CheMed123"
]


# Path to save scraped data
base_dir = "data/raw/telegram_messages"

async def scrape_channel(channel):
    await client.start()
    messages = []
    today = datetime.now().strftime('%Y-%m-%d')
    save_path = os.path.join(base_dir, today)
    os.makedirs(save_path, exist_ok=True)

    async for msg in client.iter_messages(channel, limit=100):  # adjust limit if needed
        record = {
            "id": msg.id,
            "date": str(msg.date),
            "message": msg.message,
            "has_media": bool(msg.media),
        }
        if isinstance(msg.media, MessageMediaPhoto):
            filename = f"{channel.replace('https://t.me/', '')}_{msg.id}.jpg"
            image_dir = os.path.join("data", "raw", "images", today)
            os.makedirs(image_dir, exist_ok=True)
            await msg.download_media(file=os.path.join(image_dir, filename))
            record["media_file"] = filename

        messages.append(record)

    filename = os.path.join(save_path, f"{channel.split('/')[-1]}.json")
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(messages, f, indent=2)

    print(f"Scraped {len(messages)} messages from {channel} into {filename}")

with client:
    for ch in channels:
        print(f"Scraping channel: {ch}")
        client.loop.run_until_complete(scrape_channel(ch))
