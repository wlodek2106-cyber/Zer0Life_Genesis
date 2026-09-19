import os
import sys
import logging
from aiohttp import web
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.web_hook import SimpleRequestHandler, setup_application

logging.basicConfig(level=logging.INFO, stream=sys.stdout)

TOKEN = os.getenv("BOT_TOKEN")
PORT = int(os.getenv("PORT", 10000))
WEBHOOK_URL = f"https://zerolife-genesis.onrender.com"  # Укажи свой URL на Render

if not TOKEN:
    logging.error("BOT_TOKEN is not set!")
    sys.exit(1)

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(commands=["start"])
async def cmd_start(message: types.Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🎮 Играть", url="https://t.me/your_game_link")],
            [InlineKeyboardButton(text="💎 Купить ZRL", url="https://t.me/your_token_link")]
        ]
    )
    # Пример отправки видео с текстом и кнопками
    video_url = "https://example.com/your_video.mp4" # Замени на ссылку на видео
    await message.answer_video(
        video=video_url,
        caption="Добро пожаловать в Zer0Life! Выбери действие:",
        reply_markup=keyboard
    )

async def on_startup(bot: Bot):
    await bot.set_webhook(f"{WEBHOOK_URL}/webhook")

def main():
    app = web.Application()
    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
    )
    webhook_requests_handler.register(app, path="/webhook")
    app.on_startup.append(lambda _: on_startup(bot))
    web.run_app(app, host="0.0.0.0", port=PORT)

if __name__ == "__main__":
    main()
