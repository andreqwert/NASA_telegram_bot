from data_processing import check_file_under_limit
from telegram import InputMediaPhoto
import time


def post_one_photo(bot, image_path, telegram_chat_id, limit_mb=20.0, publication_freq_sec=5):
    """
    Отправить одно фото в tg-чат <telegram_chat_id>"""
    
    file_under_limit = check_file_under_limit(image_path, limit_mb)
    if file_under_limit:
        with open(image_path, 'rb') as img:
            image_to_send = InputMediaPhoto(media=img)
        time.sleep(publication_freq_sec)
        bot.send_media_group(chat_id=telegram_chat_id, media=[image_to_send])