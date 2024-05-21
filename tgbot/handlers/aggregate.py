import json

from aiogram import Router
from aiogram.types import Message

from tgbot.services.validators.input_validator import InputData

aggregate_router = Router()


@aggregate_router.message()
async def user_start(message: Message):
    text_to_json = json.loads(message.text)
    input_data = InputData(**text_to_json)
    await message.answer(text=str(input_data))
