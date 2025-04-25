from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters import Command

router = Router()
from aiogram.types import FSInputFile


flowers = {
    '1': {'name': '15 Роз "Испания"', 'price': 15000, 'image': 'https://example.com/ispaniya.jpg'},
    '2': {'name': '15 Роз "Ред Наоми"', 'price': 3500, 'image': 'https://example.com/rednaomi.jpg'}
}


cart = {}


@router.message(Command("product"))
async def show_products(message: Message):
    user_id = message.from_user.id
    for fid, flower in flowers.items():
        builder = InlineKeyboardBuilder()
        builder.button(text="🛒 Savatga qo‘shish", callback_data=f"add_{fid}")

        await message.bot.send_photo(
            chat_id=message.chat.id,
            photo=flower['image'],
            caption=f"{flower['name']}\nNarxi: {flower['price']} so'm",
            reply_markup=builder.as_markup()
        )
    await message.answer("Buyurtma berish uchun /cart buyrug'ini yuboring")


@router.callback_query(F.data.startswith("add_"))
async def add_to_cart(callback: CallbackQuery):
    user_id = callback.from_user.id
    flower_id = callback.data.split("_")[1]

    if user_id not in cart:
        cart[user_id] = []
    cart[user_id].append(flower_id)

    await callback.answer("🛒 Savatga qo‘shildi!")


@router.message(Command("cart"))
async def view_cart(message: Message):
    user_id = message.from_user.id
    if user_id not in cart or not cart[user_id]:
        await message.answer("Savat bo‘sh.")
        return

    text = "🧺 Savatingiz:\n"
    total = 0
    for fid in cart[user_id]:
        f = flowers.get(fid)
        if f:
            text += f"- {f['name']} — {f['price']} so‘m\n"
            total += f['price']

    text += f"\n💰 Umumiy: {total} so‘m"
    await message.answer(text)
