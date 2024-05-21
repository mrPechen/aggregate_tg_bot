import json

from aiogram import Router
from aiogram.types import Message

aggregate_router = Router()


@aggregate_router.message()
async def user_start(message: Message):
    text_to_json = json.loads(message.text)
    await message.answer(text=str(text_to_json))
