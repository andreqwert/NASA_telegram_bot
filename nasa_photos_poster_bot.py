import telegram
from telegram import InputMediaPhoto
from environs import Env
import random
import os
import argparse
import time


def parse_args():

    parser = argparse.ArgumentParser(description='Бот для постинга фото')
    parser.add_argument('images_dir', help='Путь до папки с картинками, подлежащими публикации')
    parser.add_argument('--limit_mb', default=20.0, help='Лимит (в мб.) для изображения, подлежащего публикации')
    args = parser.parse_args()
    return args


def get_random_image_path(dir_with_images):
    """
    Получаем список файлов из папки dir_with_images и перемешиваем его.
    На выход подаем первый файл из списка"""

    image_paths = []
    for root, dirs, files in os.walk(os.path.abspath(dir_with_images)):
        for file in files:
            if not file.startswith('.'):
                image_paths.append(os.path.join(root, file))
    random.shuffle(image_paths)
    return image_paths[0]


def check_file_under_limit(file_path, limit=20.0):
    """
    Проверяем, действительно ли файл по указанному пути.
    Если да, то занимает ли он больше limit мб."""

    isfile = os.path.isfile(file_path)
    if isfile:
        file_size_mb = os.stat(file_path).st_size / 1e6
        return file_size_mb < float(limit)
    else:
        return False


def main():

    args = parse_args()
    images_dir = args.images_dir
    limit_mb = args.limit_mb

    env = Env()
    env.read_env()
    telegram_bot_token = env('TELEGRAM_BOT_TOKEN')
    telegram_chat_id = env('TELEGRAM_CHAT_ID')
    publication_freq_seconds = int(env('PUBLICATION_FREQ_SECONDS'))
    bot = telegram.Bot(token=telegram_bot_token)

    while True:
        random_image_path = get_random_image_path(images_dir)
        file_under_limit = check_file_under_limit(random_image_path, limit_mb)
        if file_under_limit:
            image_to_send = InputMediaPhoto(media=open(random_image_path, 'rb'))
            time.sleep(publication_freq_seconds)
            bot.send_media_group(chat_id=-1001643643093, media=[image_to_send])
    

if __name__ == '__main__':
    main()

