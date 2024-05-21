from functools import wraps

from tgbot.database.setup import get_session


def with_session(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        async with get_session() as session:
            return await func(*args, **kwargs, session=session)

    return wrapper
