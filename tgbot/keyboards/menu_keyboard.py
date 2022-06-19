from typing import Optional

from aiogram.dispatcher.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from tgbot.dal.db_django_commands import get_categories, count_items


class NumbersCallbackFactory(CallbackData, prefix="fabnum"):
    action: str
    value: Optional[int]


async def categories_keyboard():
    CURRENT_LEVEL = 0
    builder = InlineKeyboardBuilder()
    categories = await get_categories()
    for category in categories:
        count = await count_items(category.category_code)
        builder.button(
            text=f"{category.category_name} ({count})", callback_data=NumbersCallbackFactory(action="change", value=-2)
        )

    # for category in categories:
    #     number_of_items = await count_items(category.category_code)


    return builder.as_markup()

