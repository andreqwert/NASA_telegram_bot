from data_processing import define_file_extension, download_single_image, filter_nans
import requests
import os
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

    all_photo_links = [page.get('url') for page in response.json() if page.get('media_type') == 'image']
    valid_links = filter_nans(all_photo_links)
    if not valid_links:
        print('There are no any valid links')
    for num, url in enumerate(valid_links):
        ext = define_file_extension(url)
        path_to_save = os.path.join(images_dir, f'nasa_apod_{num}{ext}')
        download_single_image(url, path_to_save)


if __name__ == '__main__':

    env = Env()
    env.read_env()
    api_key = env('API_NASA_SITE_TOKEN')

    parser = argparse.ArgumentParser(description='Скачиваем фото Earth Polychromatic Imaging Camera (EPIC)')
    parser.add_argument('--save_dir', default='images/nasa_images', type=Path, help='Путь для сохранения картинок')
    parser.add_argument('--images_num', default=50, help='Сколько скачивать изображений')
    args = parser.parse_args()

    save_dir = Path.cwd().joinpath(args.save_dir)
    images_num = args.images_num

    os.makedirs(save_dir, exist_ok=True)
    fetch_nasa_images(api_key, save_dir, images_num=images_num)

