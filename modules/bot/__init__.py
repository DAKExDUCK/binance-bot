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


async def send(chat_id, text, link):
    markup = types.InlineKeyboardMarkup()
    link_button = types.InlineKeyboardButton(text='Order Link', url=link)
    markup.add(link_button)
    try:
        return await bot.send_message(chat_id, text)
        # return await bot.send_message(chat_id, text, reply_markup=markup)
    except exceptions.BotBlocked:
        ...
    except exceptions.ChatNotFound:
        ...
    except exceptions.RetryAfter as e:
        await asyncio.sleep(e.timeout)
        return await send(chat_id, text)
    except exceptions.UserDeactivated:
        ...
    except exceptions.TelegramAPIError:
        logger.error(f"{chat_id}\n{text}\n", exc_info=True)