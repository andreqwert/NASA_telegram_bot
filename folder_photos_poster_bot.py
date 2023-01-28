import telegram
from environs import Env
import os
import argparse
from data_processing import get_random_image_path
from tg_functions import post_one_photo
from pathlib import Path


def parse_args():

    parser = argparse.ArgumentParser(description='Бот для постинга фото. Публикуются случайные фото из папки.')
    parser.add_argument('--images_dir', default='./images/', type=Path, help='Путь до папки с картинками, подлежащими публикации (в случае, если не указано определенное фото).')
    parser.add_argument('--limit_mb', default=20.0, type=float, help='Лимит (в мб.) для изображения, подлежащего публикации')
    parser.add_argument('--publication_freq_sec', default=5, type=int, help='Частота публикации в канале Telegram (в секундах)')
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
    images_dir = args.images_dir
    limit_mb = args.limit_mb
    publication_freq_sec = args.publication_freq_sec
    retry_delay_seconds = args.retry_delay_seconds

    assert len(os.listdir(images_dir)) > 0, 'Images directory is empty'

    while True:
        try:
            image_path = get_random_image_path(images_dir)
            post_one_photo(bot, image_path, telegram_chat_id, limit_mb=limit_mb, publication_freq_sec=publication_freq_sec)
        except telegram.error.NetworkError:
            print(f"Received ConnectionError. Retrying in {retry_delay_seconds} seconds...")
            telegram.error.RetryAfter(retry_delay_seconds)
    

if __name__ == '__main__':
    main()
