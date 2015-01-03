__author__ = 'JennyYueJin'

from pprint import pprint
import os

import shutil
import requests
import urlparse
from bs4 import BeautifulSoup


def get_soup(url):
    """
    :param url: link to the page
    :return: soup object
    """

    responseText = requests.get(url).text

    return BeautifulSoup(responseText)


def get_page_video_urls():
    """
    Get all video links from a webpage
    Tutorial at http://blog.miguelgrinberg.com/post/easy-web-scraping-with-python
    :return:
    """
    root_url = 'http://pyvideo.org'
    index_url = root_url + '/category/50/pycon-us-2014'

    soup = get_soup(index_url)
    return [root_url + a.attrs.get('href') for a in soup.select('div.video-summary-data a[href^=/video]')]


def get_page_image_urls(pageLink):

    soup = get_soup(pageLink)

    for tag in soup.find_all('img'):
        r = tag.get('src')
        if r is not None:
            yield r


def download_pic(link, outputDir):
    """
    downloads a single pic
    :return: output file path
    """

    # get pic object
    rawPic = requests.get(link, stream=True).raw

    # write to file
    outputFpath = os.path.join(outputDir, os.path.basename(urlparse.urlparse(link).path))

    with open(outputFpath, 'wb') as f:
        shutil.copyfileobj(rawPic, f)

    # clean up
    del rawPic


imgOutputDir = '/Users/JennyYueJin/ProjectHI/Scraping/output'

list(get_page_image_urls('https://plus.google.com/photos/+HawaiianPaddleSports/albums/6097270274560596833'))

pprint(list(get_page_image_urls('https://www.facebook.com/')))

download_pic('https://lh6.googleusercontent.com/_FEVkydLItTgYfvxmyQXPKG0B1Fo2yq5br3wRg2Mc5Nd=w1477-h1108-no', imgOutputDir)

for picLink in get_page_image_urls('https://www.facebook.com/'):
    print picLink
    download_pic(picLink, imgOutputDir)

