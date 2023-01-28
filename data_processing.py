import requests
from os.path import splitext
from urllib.parse import unquote, urlsplit
import random
import os


def get_quotefree_url(url):
    """Get clear url without quotes and additional fragments"""

    return urlsplit(unquote(url))._replace(fragment="", query="").geturl() 


def define_file_extension(url):
    """Define from the url what extension the image has."""

    quotefree_url = get_quotefree_url(url)
    _, ext = splitext(quotefree_url)
    return ext


def download_single_image(url, path_to_save):

    response = requests.get(url, verify=True)
    response.raise_for_status()

    with open(path_to_save, 'wb') as f:
        f.write(response.content)


def filter_nans(lst):
    return [elem for elem in lst if elem is not None]


def convert_to_mb(size_in_bytes):
    return size_in_bytes / (1024 * 1024)


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
    Проверяем, действительно ли существует файл по указанному пути.
    Если да, то занимает ли он больше limit мб.
    На выходе - булева переменная"""

    isfile = os.path.isfile(file_path)
    if isfile:
        file_size_mb = convert_to_mb(os.stat(file_path).st_size)
        return file_size_mb < float(limit)
    else:
        print(f'Recheck file path or file is invalid: {file_path}')
        return False






