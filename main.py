import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config import API_TOKEN
from handlers import register, start, cart
from aiogram.client.bot import DefaultBotProperties

async def main():
    bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_routers(start.router, register.router, cart.router)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())








# from aiogram import Bot, Dispatcher, types
# from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
# from aiogram.utils import executor
# from aiogram.dispatcher import FSMContext
# from aiogram.contrib.fsm_storage.memory import MemoryStorage
# from aiogram.dispatcher.filters.state import State, StatesGroup
# import logging
#
# API_TOKEN = '8042642586:AAFsKL4EIvO_Ii-qe0c7dXbRn8AE2X10WGc'
# ADMIN_ID = 1893873090  # o'zingizning Telegram ID'ingizni yozing
#
# logging.basicConfig(level=logging.INFO)
#
# bot = Bot(token=API_TOKEN)
# storage = MemoryStorage()
# dp = Dispatcher(bot, storage=storage)
#
# # Mahsulotlar
# flowers = {
#     '1': {
#         'name': '15 Роз "Испания"',
#         'price': 15000,
#         'image': 'https://example.com/ispaniya.jpg'
#     },
#     '2': {
#         'name': '15 Роз "Ред Наоми"',
#         'price': 3500,
#         'image': 'https://example.com/rednaomi.jpg'
#     }
# }
#
# # Savat va foydalanuvchi ma'lumotlari
# cart = {}
# user_data = {}
#
# # Holatlarni aniqlash
# class Register(StatesGroup):
#     name = State()
#     phone = State()
#     address = State()
#     payment = State()
#
# # /start komandasi
# @dp.message_handler(commands=['start'])
# async def send_welcome(message: types.Message):
#     for key, flower in flowers.items():
#         markup = InlineKeyboardMarkup().add(
#             InlineKeyboardButton("🛒 Savatga qo‘shish", callback_data=f"add_{key}")
#         )
#         caption = f"{flower['name']}\nNarxi: {flower['price']} руб."
#         await bot.send_photo(
#             message.chat.id,
#             photo=flower['image'],
#             caption=caption,
#             reply_markup=markup
#         )
#     await message.answer("📝 Buyurtma berish uchun /register buyrug'ini yuboring")
#
# # Mahsulot savatga qo'shish
# @dp.callback_query_handler(lambda c: c.data.startswith('add_'))
# async def add_to_cart(callback_query: types.CallbackQuery):
#     user_id = callback_query.from_user.id
#     flower_id = callback_query.data.split('_')[1]
#
#     if user_id not in cart:
#         cart[user_id] = []
#     cart[user_id].append(flower_id)
#
#     await callback_query.answer("🧺 Savatga qo‘shildi!")
#
# # /cart komandasi - savatni ko'rish
# @dp.message_handler(commands=['cart'])
# async def view_cart(message: types.Message):
#     user_id = message.from_user.id
#     if user_id not in cart or not cart[user_id]:
#         await message.answer("Savat bo‘sh")
#         return
#
#     text = "🧺 Sizning savatingiz:\n"
#     total = 0
#     for fid in cart[user_id]:
#         flower = flowers[fid]
#         text += f"- {flower['name']} — {flower['price']} руб.\n"
#         total += flower['price']
#     text += f"\n💵 Jami: {total} руб."
#     await message.answer(text)
#
# # /register komandasi
# @dp.message_handler(commands=['register'])
# async def start_register(message: types.Message):
#     await message.answer("👤 Ismingizni kiriting:")
#     await Register.name.set()
#
# @dp.message_handler(state=Register.name)
# async def get_name(message: types.Message, state: FSMContext):
#     await state.update_data(name=message.text)
#     await message.answer("📞 Telefon raqamingizni kiriting:")
#     await Register.next()
#
# @dp.message_handler(state=Register.phone)
# async def get_phone(message: types.Message, state: FSMContext):
#     await state.update_data(phone=message.text)
#     await message.answer("🏠 Yetkazib berish manzilingiz:")
#     await Register.next()
#
# @dp.message_handler(state=Register.address)
# async def get_address(message: types.Message, state: FSMContext):
#     await state.update_data(address=message.text)
#     markup = InlineKeyboardMarkup()
#     markup.add(InlineKeyboardButton("💵 Naqd", callback_data="pay_cash"))
#     markup.add(InlineKeyboardButton("📲 Click/Payme", callback_data="pay_online"))
#     await message.answer("💳 To‘lov turini tanlang:", reply_markup=markup)
#     await Register.next()
#
# @dp.callback_query_handler(lambda c: c.data.startswith('pay_'), state=Register.payment)
# async def payment_method(callback_query: types.CallbackQuery, state: FSMContext):
#     payment = "Naqd" if callback_query.data == "pay_cash" else "Click/Payme"
#     await state.update_data(payment=payment)
#     data = await state.get_data()
#
#     user_id = callback_query.from_user.id
#     total = 0
#     products = ""
#     for fid in cart.get(user_id, []):
#         f = flowers[fid]
#         total += f['price']
#         products += f"- {f['name']} ({f['price']} руб.)\n"
#
#     summary = (
#         f"🧾 Buyurtma:\n"
#         f"👤 Ism: {data['name']}\n"
#         f"📞 Tel: {data['phone']}\n"
#         f"🏠 Manzil: {data['address']}\n"
#         f"📦 Mahsulotlar:\n{products}\n💰 Jami: {total} руб.\n💳 To‘lov turi: {data['payment']}"
#     )
#
#     await bot.send_message(callback_query.from_user.id, "✅ Buyurtmangiz qabul qilindi! Rahmat!")
#     await bot.send_message(ADMIN_ID, summary)
#     await callback_query.answer()
#     await state.finish()
#
# if __name__ == '__main__':
#     executor.start_polling(dp, skip_updates=True)
#
#
# #
# #
# #
# #
