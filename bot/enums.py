from enum import Enum


class ErrorMessage(Enum):
    SIZE_LIMIT = "⚠️ К сожалению, из-за ограничений телеграма, мы не можем отправлять видео больше 50 мегабайт. Попытка выложить файл на filebin.net"
    GENERAL_ERROR = "⚠️ Произошла ошибка."
    MULTIPLE_VIDEOS_ERROR = "⚠️ Пожалуйста, подождите пока скачается прошлое видео и повторите снова."
    YT_DLP_ERROR = "⚠️ Видео могло не скачаться из-за особенностей хостинга. Попробуйте наше зеркало (работает не 24/7):\n\n<b>@free_yt_dl_mirror_bot</b>"


class StatusMessage(Enum):
    PREPARING = "⏳ Файл подготавливается. Пожалуйста, подождите немного."
    PROMO = "Привет! Я <b>@free_yt_dl_bot</b> — полностью бесплатный, без рекламы и обязательных подписок. Если тебе нравится моя работа, загляни на мой <b><a href='https://t.me/anekobtw_c'>телеграм канал с новостями</a></b> — это большая поддержка для меня! 😊\n\n<b>Это сообщение самоудалится через 10 секунд</b>"
    BOT_CAPTION = "<b>@free_yt_dl_bot</b>"


class Links(Enum):
    YOUTUBE = [
        "https://www.youtube.com/",
        "https://youtu.be/",
        "https://www.youtube.com/shorts/",
        "https://youtube.com/shorts/",
    ]
    STANDART = [
        "https://www.tiktok.com/",
        "https://vt.tiktok.com/",
        "https://vm.tiktok.com/",
        "https://www.instagram.com/reel/",
        "https://instagram.com/reel/",
        "https://www.instagram.com/share/",
        "https://x.com/",
        "https://twitter.com/",
    ]
