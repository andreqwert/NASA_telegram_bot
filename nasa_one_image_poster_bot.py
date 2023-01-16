import telegram
import requests
from telegram import InputMediaPhoto
from environs import Env
import argparse
import time
from data_processing import convert_to_mb, get_random_image_path, check_file_under_limit


def parse_args():

    parser = argparse.ArgumentParser(description='Бот для постинга фото. Если явно фото не укзаано, то публикается случайное фото.')
    parser.add_argument('--user_image_path', help='Путь до изображения для публикации. Если флаг указан, то это из-е будет загружено первым.')
    parser.add_argument('--limit_mb', default=20.0, type=float, help='Лимит (в мб.) для изображения, подлежащего публикации')
    parser.add_argument('--retry_delay_seconds', default=5, type=int, help='Через сколько секунд будет произведен повторный запрос при потере соединения')
    args = parser.parse_args()
    return args


def main():

    env = Env()
    env.read_env()
    telegram_bot_token = env('TELEGRAM_BOT_TOKEN')
    telegram_chat_id = env('TELEGRAM_CHAT_ID')
    bot = telegram.Bot(token=telegram_bot_token)

    args = parse_args()
    user_image_path = args.user_image_path
    limit_mb = args.limit_mb
    retry_delay_seconds = args.retry_delay_seconds

    try:
        if user_image_path:
            image_path = user_image_path
        else:
            image_path = get_random_image_path(images_dir)
        file_under_limit = check_file_under_limit(image_path, limit_mb)
        if file_under_limit:
            with open(image_path, 'rb') as img:
                image_to_send = InputMediaPhoto(media=img)
            bot.send_media_group(chat_id=178680093, media=[image_to_send])
    except telegram.error.NetworkError:
        print(f"Received ConnectionError. Retrying in {retry_delay_seconds} seconds")
        telegram.error.RetryAfter(retry_delay_seconds)
    

if __name__ == '__main__':
    main()

