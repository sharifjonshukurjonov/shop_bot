from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from keyboards.inline import get_region_keyboard, get_district_keyboard
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import json

router = Router()

class Register(StatesGroup):
    name = State()
    phone = State()
    region = State()
    district = State()
    address = State()
    payment = State()

@router.message(F.text == "/register")
async def register_start(message: Message, state: FSMContext):
    await message.answer("👤 Ismingizni kiriting:")
    await state.set_state(Register.name)

@router.message(Register.name)
async def get_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("📞 Telefon raqamingizni kiriting:")
    await state.set_state(Register.phone)

@router.message(Register.phone)
async def get_phone(message: Message, state: FSMContext):
    await state.update_data(phone=message.text)
    await message.answer("🏢 Viloyatingizni tanlang:", reply_markup=get_region_keyboard())
    await state.set_state(Register.region)

@router.callback_query(Register.region)
async def get_region(callback: CallbackQuery, state: FSMContext):
    region = callback.data.split(":")[1]
    await state.update_data(region=region)
    await callback.message.answer("📍 Tumanni tanlang:", reply_markup=get_district_keyboard(region))
    await state.set_state(Register.district)

@router.callback_query(Register.district)
async def get_district(callback: CallbackQuery, state: FSMContext):
    district = callback.data.split(":")[1]
    await state.update_data(district=district)
    await callback.message.answer("📬 To‘liq manzilingizni kiriting:")
    await state.set_state(Register.address)

@router.message(Register.address)
async def get_address(message: Message, state: FSMContext):
    await state.update_data(address=message.text)

    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="💵 Naqd", callback_data="pay_cash")],
            [InlineKeyboardButton(text="📲 Click/Payme", callback_data="pay_online")]
        ]
    )

    await message.answer("💳 To‘lov turini tanlang:", reply_markup=markup)
    await state.set_state(Register.payment)

@router.callback_query(Register.payment)
async def get_payment(callback: CallbackQuery, state: FSMContext):
    payment = "Naqd" if callback.data == "pay_cash" else "Click/Payme"
    await state.update_data(payment=payment)

    data = await state.get_data()

    user = {
        "tg_id": str(callback.from_user.id),
        "name": data["name"],
        "phone": data["phone"],
        "region": data["region"],
        "district": data["district"],
        "address": data["address"],
        "payment": data["payment"]
    }

    with open("data/users.json", "r+") as f:
        users = json.load(f)
        users.append(user)
        f.seek(0)
        json.dump(users, f, indent=2)

    await callback.message.answer("✅ Ro‘yxatdan o‘tish yakunlandi!")
    await callback.answer()
    await state.clear()
