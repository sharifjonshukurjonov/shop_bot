from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


regions = ["Toshkent", "Samarqand", "Andijon"]


districts = {
    "Toshkent": ["Yunusobod", "Chilonzor", "Mirzo Ulug‘bek"],
    "Samarqand": ["Urgut", "Kattaqo‘rg‘on", "Narpay"],
    "Andijon": ["Asaka", "Shahrixon", "Xonobod"]
}


def get_region_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text=region, callback_data=f"region:{region}")]
        for region in regions
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

# Tanlangan viloyatga qarab tumanlarni chiqarish
def get_district_keyboard(region: str) -> InlineKeyboardMarkup:
    district_list = districts.get(region, [])
    buttons = [
        [InlineKeyboardButton(text=district, callback_data=f"district:{district}")]
        for district in district_list
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
