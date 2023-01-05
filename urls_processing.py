import requests
import os
from os.path import splitext
from urllib.parse import unquote, urlsplit


def get_quotefree_url(url):
    """Get clear url without quotes and additional fragments"""

    return urlsplit(unquote(url))._replace(fragment="", query="").geturl() 


def define_file_extenstion(url):
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




