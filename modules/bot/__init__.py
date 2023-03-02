import asyncio

from aiogram import types
from aiogram.utils import exceptions
from config import bot
from modules.logger import logger


def clear_MD(text: str) -> str:
    text = str(text)
    symbols = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']

    for sym in symbols:
        text = text.replace(sym, f"\{sym}")

    return text


async def send(chat_id, text):
    try:
        return await bot.send_message(chat_id, text)
    except Exception as exc:
        logger.error(exc, exc_info=True)
        