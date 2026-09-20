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
            [InlineKeyboardButton(text="🎮 Play", url="https://t.me/Zer0lifelabs_ai_bot")],
            [InlineKeyboardButton(text="💎 Buy ZRL", url="https://www.ponsfamily.com/launchpad/0x09bbf85C1C1ad7518847733fc64e161557056200")],
            [InlineKeyboardButton(text="☕ Donate (SOL, ETH, BNB)", callback_data="donate_info")],
            # Кнопка роадмапа в стартовом меню
            [InlineKeyboardButton(text="Roadmap ZRL 2026-2027 🗺️", callback_data="send_roadmap_pdf")]
        ]
    )
    
    video_file_id = "BAACAgIAAxkBAAIrGWqujnZn-ijNnIrt_gJsams6kowAAymuAAJ39GhJYt62HlDP-GE9BA"
    
    caption_text = "Welcome to Zer0Life! Choose an action:"
    
    await message.answer_video(
        video=video_file_id,
        caption=caption_text,
        reply_markup=keyboard
    )

# Обработчик нажатия на кнопку донатов
@dp.callback_query(F.data == "donate_info")
async def process_donate(callback: types.CallbackQuery):
    donate_text = (
        "☕ **Support the project:**\n\n"
        "🔹 **Solana (SOL):**\n`5HX8uQvTE27DK27pRudHBGAy1EfR6uupDZssqkk3Yrpz`\n\n"
        "🔹 **Ethereum (ETH):**\n`0x7901D7566766379f9ffc11326762883D6161183f`\n\n"
        "🔹 **BNB (BSC):**\n`0x7901D7566766379f9ffc11326762883D6161183f`\n\n"
        "Thank you for supporting Zer0Life! 🙏"
    )
    await callback.message.answer(donate_text, parse_mode="Markdown")
    await callback.answer()

# Обработчик для отправки PDF с обновленным file_id
@dp.callback_query(F.data == "send_roadmap_pdf")
async def process_roadmap(callback: types.CallbackQuery):
    await callback.answer() # Убираем часики загрузки с кнопки
    roadmap_file_id = "BQACAgIAAxkBAAIraGqvnxP_eZvrrmMF9FkLNGKbK9F7AAIrowAC7ol5SZM2l2KFXMD3PQQ"
    await callback.message.answer_document(
        document=roadmap_file_id,
        caption="Roadmap ZRL 2026-2027 🗺️"
    )

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
