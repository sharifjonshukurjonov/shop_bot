from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
import json
import os

router = Router()

@router.message(F.text == "/start")
async def start_handler(message: Message):
    btn = InlineKeyboardButton(
        text="🔐 Login", callback_data=f"login:{message.from_user.id}"
    )
    kb = InlineKeyboardMarkup(inline_keyboard=[[btn]])
    await message.answer("👋 Salom! Botga xush kelibsiz!", reply_markup=kb)

@router.callback_query(F.data.startswith("login:"))
async def login_handler(callback):
    user_id = str(callback.from_user.id)
    if not os.path.exists("data/users.json"):
        with open("data/users.json", "w") as f:
            json.dump([], f)

    with open("data/users.json", "r") as f:
        users = json.load(f)

    if any(user["tg_id"] == user_id for user in users):
        await callback.message.answer("✅ Siz allaqachon ro‘yxatdan o‘tgansiz!")
    else:
        await callback.message.answer("📝 Ro‘yxatdan o‘tish uchun /register buyrug'ini yuboring.")

    await callback.answer()
