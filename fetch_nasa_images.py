from urls_processing import define_file_extenstion, download_single_image
import requests
import os
from urllib.parse import urlencode
import argparse
from environs import Env
from pathlib import Path


def fetch_nasa_images(api_key, images_dir, images_num=50):

    payload = {
        'api_key': api_key,
        'count': images_num
    }

    response = requests.get('https://api.nasa.gov/planetary/apod', params=payload, verify=True)
    response.raise_for_status()

    photo_links = [page.get('url') for page in response.json() if page.get('media_type') == 'image']
    for num, url in enumerate(photo_links):
        ext = define_file_extenstion(url)
        path_to_save = os.path.join(images_dir, f'nasa_apod_{num}{ext}')
        download_single_image(url, path_to_save)


if __name__ == '__main__':

    env = Env()
    env.read_env()
    api_key = env('API_TOKEN')

    parser = argparse.ArgumentParser(description='Скачиваем фото Earth Polychromatic Imaging Camera (EPIC)')
    parser.add_argument('--save_dir', default=['images', 'nasa_images'], help='Путь для сохранения картинок')
    parser.add_argument('--images_num', default=50, help='Сколько скачивать изображений')
    args = parser.parse_args()

    save_dir = Path.cwd().joinpath(*args.save_dir)
    images_num = args.images_num

    os.makedirs(save_dir, exist_ok=True)
    fetch_nasa_images(api_key, save_dir, images_num=images_num)

