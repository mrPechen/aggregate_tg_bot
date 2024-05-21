import json

from aiogram import Router
from aiogram.types import Message

from tgbot.services.factory import DataAggregator
from tgbot.services.validators.input_validator import InputData

aggregate_router = Router()


@aggregate_router.message()
async def user_start(message: Message):
    try:
        text_to_json = json.loads(message.text)
        input_data = InputData(**text_to_json)
        result = await DataAggregator().aggregate(input_data)
        await message.answer(text=json.dumps(result))

    except ValueError as e:
        try:
            await message.answer(text=str(e.errors()[0]["ctx"]["error"]))
        except Exception:
            await message.answer(text='Невалидный запос. Пример запроса:\n'
                                      '{"dt_from": "2022-09-01T00:00:00", "dt_upto": "2022-12-31T23:59:00", "group_type": "month"}')
