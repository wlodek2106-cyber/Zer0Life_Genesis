import os
import sys
import logging
from aiohttp import web
from aiogram import Bot, Dispatcher, F, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

logging.basicConfig(level=logging.INFO, stream=sys.stdout)

TOKEN = os.getenv("BOT_TOKEN")
PORT = int(os.getenv("PORT", 10000))
WEBHOOK_URL = f"https://zer0life-genesis.onrender.com"

if not TOKEN:
    logging.error("BOT_TOKEN is not set!")
    sys.exit(1)

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(F.text == "/start")
async def cmd_start(message: types.Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🎮 Играть", url="https://t.me/your_game_link")],
            [InlineKeyboardButton(text="💎 Купить ZRL", url="https://t.me/your_token_link")]
        ]
    )
    await message.answer("Добро пожаловать в Zer0Life! Выбери действие:", reply_markup=keyboard)

# Бот поймает видео и пришлет правильный file_id в чат
@dp.message(F.video)
async def get_video_id(message: types.Message):
    file_id = message.video.file_id
    await message.answer(f"Твой правильный file_id:\n`{file_id}`", parse_mode="Markdown")

async def on_startup(bot: Bot):
    await bot.set_webhook(f"{WEBHOOK_URL}/webhook", drop_pending_updates=True)

def main():
    app = web.Application()
    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
    )
    webhook_requests_handler.register(app, path="/webhook")
    setup_application(app, dp, bot=bot)
    app.on_startup.append(lambda _: on_startup(bot))
    web.run_app(app, host="0.0.0.0", port=PORT)

if __name__ == "__main__":
    main()
