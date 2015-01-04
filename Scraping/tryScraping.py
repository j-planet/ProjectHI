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


def is_full_url(url):
    """
    './blah' -> false; 'http://google.com' -> true
    :return: Boolean
    """

    return urlparse.urlparse(url).scheme != ''


def extract_root_url(url):
    """
    http://google.com/blahblah -> http://google.com
    :return: string. Raises exception if url doesn't contain a root url (e.g. './blahblah')
    """

    if not is_full_url(url):
        raise ValueError('The given url (%s) contains no root url.' % url)

    temp = urlparse.urlparse(url)
    scheme = temp.scheme
    netloc = temp.netloc

    return scheme + '://' + netloc


def make_full_url(link, urlWithScheme = None):
    """
    returns the original url if it's already full
    :return: string
    """

    if is_full_url(link):
        return link
    else:
        return urlparse.urljoin(extract_root_url(urlWithScheme), link)


def download_pic(link, outputDir, suffix=None, homeUrl=None):
    """
    downloads a single pic
    :param suffix: extra string to insert at the end of the file name
    :param homeUrl: an URL containing the root/base url. not needed if the link is already a full url
    :return: output file path
    """

    # get pic object
    rawPic = requests.get(make_full_url(link, homeUrl), stream=True).raw

    # write to file
    name, ext = os.path.splitext(os.path.basename(urlparse.urlparse(link).path))
    filename = name + ('' if suffix is None else '_' + str(suffix)) + '.' + ext

    outputFpath = os.path.join(outputDir, filename)

    with open(outputFpath, 'wb') as f:
        shutil.copyfileobj(rawPic, f)

    # clean up
    del rawPic


pageURL = 'http://bloomingdalesfashionpacked.com/closet-what-to-wear-where.aspx?cm_sp=NAVIGATION-_-TOP_NAV-_-2910-CATEGORY_ICON_IMAGE-January---What-to-Wear-Where#closet'
imgOutputDir = '/Users/JennyYueJin/ProjectHI/Scraping/output'

# pprint(list(get_page_image_urls(pageURL)))

for counter, picLink in enumerate(get_page_image_urls(pageURL)):
    print picLink
    download_pic(picLink, imgOutputDir, suffix=counter, homeUrl=pageURL)

