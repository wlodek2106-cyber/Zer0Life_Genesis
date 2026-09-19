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
            [InlineKeyboardButton(text="🎮 Play / Играть", url="https://t.me/Zer0lifelabs_ai_bot")],
            [InlineKeyboardButton(text="💎 Buy ZRL / Купить ZRL", url="https://t.me/your_token_link")],
            [InlineKeyboardButton(text="☕ Донаты / Donate (SOL, ETH, BNB)", callback_data="donate_info")]
        ]
    )
    
    video_file_id = "BAACAgIAAxkBAAIrGWqujnZn-ijNnIrt_gJsams6kowAAymuAAJ39GhJYt62HlDP-GE9BA"
    
    caption_text = (
        "Welcome to Zer0Life! Choose an action:\n\n"
        "Добро пожаловать в Zer0Life! Выбери действие:"
    )
    
    await message.answer_video(
        video=video_file_id,
        caption=caption_text,
        reply_markup=keyboard
    )

# Обработчик нажатия на кнопку донатов
@dp.callback_query(F.data == "donate_info")
async def process_donate(callback: types.CallbackQuery):
    donate_text = (
        "☕ **Поддержать проект / Support the project:**\n\n"
        "🔹 **Solana (SOL):** `ТВОЙ_КОШЕЛЕК_SOL`\n"
        "🔹 **Ethereum (ETH):** `ТВОЙ_КОШЕЛЕК_ETH`\n"
        "🔹 **BNB (BSC):** `ТВОЙ_КОШЕЛЕК_BNB`\n\n"
        "Спасибо за поддержку Zer0Life! 🙏"
    )
    await callback.message.answer(donate_text, parse_mode="Markdown")
    await callback.answer() # Закрываем анимацию загрузки на кнопке

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
