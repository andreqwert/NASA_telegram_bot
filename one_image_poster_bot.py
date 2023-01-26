import telegram
from environs import Env
import argparse
from data_processing import get_random_image_path
from tg_functions import post_one_photo
import os
from pathlib import Path


def parse_args():

    parser = argparse.ArgumentParser(description='Бот для постинга фото. Если явно фото не укзаано, то публикается случайное фото.')
    parser.add_argument('--user_image_path', help='Путь до изображения для публикации. Если флаг указан, то это из-е будет загружено первым.')
    parser.add_argument('--images_dir', default='./images/', type=Path, help='Путь до папки с картинками, подлежащими публикации (в случае, если не указано определенное фото).')
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
    images_dir = args.images_dir
    
    if user_image_path:
        image_path = user_image_path
    else:
        assert len(os.listdir(images_dir)) > 0, 'Images directory is empty'
        image_path = get_random_image_path(images_dir)
    post_one_photo(bot, image_path, telegram_chat_id, limit_mb=limit_mb)
    

if __name__ == '__main__':
    main()
