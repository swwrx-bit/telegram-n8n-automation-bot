import asyncio
import logging
from aiogram import Bot, Dispatcher, types
import aiohttp

BOT_TOKEN = "8676960293:AAE6g6hszylaTDjwsObaWc2B3EFtc9i6OK4"
WEBHOOK_URL = "http://localhost:5678/webhook/telegram-bot"

# Configure logging
logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message()
async def handle_message(message: types.Message):
    # Only process text messages (avoid crashes if user sends media/sticker)
    text_content = message.text if message.text else ""
    user_id = message.from_user.id if message.from_user else None
    
    payload = {
        "message": text_content,
        "user_id": user_id
    }
    
    logging.info(f"Received message from {user_id}: {text_content}")
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(WEBHOOK_URL, json=payload) as response:
                res_text = await response.text()
                logging.info(f"Forwarded to n8n. Response: {res_text}")
    except Exception as e:
        logging.error(f"Error forwarding message to n8n: {e}")

async def main():
    logging.info("Starting Telegram bot...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
