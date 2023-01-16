from data_processing import define_file_extenstion, download_single_image
import requests
import os
import argparse
from pathlib import Path


def fetch_spacex_images(images_dir, launch_id=None):
    
    last_launch_url = f'https://api.spacexdata.com/v5/launches/{launch_id}/'
    response = requests.get(last_launch_url)
    response.raise_for_status()

    photo_links = response.json().get('links', {})['flickr']['original']
    if not photo_links:
        print('There are no any photo links')
    for num, url in enumerate(photo_links):
        ext = define_file_extenstion(url)
        path_to_save = os.path.join(images_dir, f'spacex{num}{ext}')
        download_single_image(url, path_to_save)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Скачиваем фото с сайта SpaceX')
    parser.add_argument('--save_dir', default='images/spacex_images', type=Path, help='Путь для сохранения картинок')
    parser.add_argument('--launch_id', default='latest', help='ID запуска. Если не указан, то парсятся фото последнего пуска')
    args = parser.parse_args()

    save_dir = Path.cwd().joinpath(args.save_dir)
    launch_id = args.launch_id
    
    os.makedirs(save_dir, exist_ok=True)    
    fetch_spacex_images(save_dir, launch_id)





    