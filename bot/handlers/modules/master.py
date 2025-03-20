import asyncio
import os
import shutil
from typing import Any, Callable

import requests
from aiogram import exceptions, types
from tenacity import retry, retry_if_exception_type, stop_after_attempt
from videoprops import get_video_properties

ERROR_MESSAGES = {
    "size_limit": "⚠️ К сожалению, из-за ограничений телеграма, мы не можем отправлять видео больше 50 мегабайт. Попытка выложить файл на filebin.net",
    "general_error": "⚠️ Произошла ошибка.",
    "multiple_videos_error": "⚠️ Пожалуйста, подождите пока скачается прошлое видео и повторите снова.",
}
currently_downloading = set()


async def async_download(func: Callable[..., Any]) -> Any:
    return await asyncio.to_thread(func)


def publish(filename: str) -> str:
    with open(filename, "rb") as file:
        headers = {"filename": filename, "Content-Type": "application/octet-stream"}
        response = requests.post(
            url="https://filebin.net",
            files={"file": file},
            data={"bin": "anekobtw"},
            headers=headers,
        )
    res = response.json()
    return f"https://filebin.net/{res['bin']['id']}/{res['file']['filename']}"


@retry(retry=retry_if_exception_type(exceptions.TelegramNetworkError), stop=stop_after_attempt(3))
async def master_handler(message: types.Message, send_function: Callable, download_function: Callable, url: str) -> None:
    if message.from_user.id in currently_downloading:
        await message.answer(ERROR_MESSAGES["multiple_videos_error"])
        return

    currently_downloading.add(message.from_user.id)
    status_msg = await message.answer(f"⏳ Файл подготавливается. Пожалуйста, подождите немного.")

    try:
        filename = await async_download(download_function)

        if filename.endswith(".mp4"):
            props = get_video_properties(filename)
            await send_function(types.FSInputFile(filename), caption="<b>@free_yt_dl_bot</b>", height=props["height"], width=props["width"])
        else:
            await send_function(types.FSInputFile(filename), caption="<b>@free_yt_dl_bot</b>")

        await message.delete()
        await status_msg.delete()

    except exceptions.TelegramEntityTooLarge:
        await status_msg.edit_text(ERROR_MESSAGES["size_limit"])
        await status_msg.edit_text(publish(filename))
        await message.delete()

    except Exception as e:
        print(e)
        await status_msg.edit_text(
            text=ERROR_MESSAGES["general_error"],
            reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(text="📩 Сообщить о проблеме (анонимно)", callback_data=f"report!{url}")]]),
        ),

    finally:
        currently_downloading.discard(message.from_user.id)
        if os.path.isfile(filename):
            os.remove(filename)
        elif os.path.isdir(filename):
            shutil.rmtree(filename)
