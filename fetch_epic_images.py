import requests
from datetime import datetime
from urls_processing import download_single_image
import os
import argparse
from environs import Env
from pathlib import Path


def construct_download_link(im_desc, api_key):

    img_name = im_desc.get('image')
    img_datetime = datetime.fromisoformat(im_desc.get('date'))
    img_date = img_datetime.date()
    year, month, day = img_date.year, img_date.month, img_date.day
    date = '{}/{:02d}/{:02d}'.format(year, month, day)

    payload = {
        'api_key': api_key,
    }

    url = f'https://api.nasa.gov/EPIC/archive/natural/{date}/png/{img_name}.png'
    response = requests.post(url, params=payload)
    response.raise_for_status()
    return response.url


def fetch_epic_images(api_key, images_dir, images_num=5):

    payload = {
        'api_key': api_key
    }

    url = 'https://api.nasa.gov/EPIC/api/natural/images/'
    response = requests.get(url, params=payload)
    response.raise_for_status()
    images_data = response.json()

    photo_links = [construct_download_link(im_desc, api_key) for im_desc in images_data[:images_num]]
    for num, url in enumerate(photo_links):
        path_to_save = os.path.join(images_dir, f'epic{num}.png')
        download_single_image(url, path_to_save)


if __name__ == '__main__':

    env = Env()
    env.read_env()
    api_key = env('API_NASA_SITE_TOKEN')

    parser = argparse.ArgumentParser(description='Скачиваем фото Earth Polychromatic Imaging Camera (EPIC)')
    parser.add_argument('--save_dir', default=['images', 'epic_images'], help='Путь для сохранения картинок')
    parser.add_argument('--images_num', default=5, help='Сколько скачивать изображений')
    args = parser.parse_args()

    save_dir = Path.cwd().joinpath(*args.save_dir)
    images_num = args.images_num

    os.makedirs(save_dir, exist_ok=True)
    fetch_epic_images(api_key, save_dir, images_num=images_num)






