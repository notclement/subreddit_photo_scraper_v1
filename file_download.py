import requests
import os
import re
from urllib.parse import urlparse
import urllib.request
import shutil

from random import randint

DUMP_PATH = './dump/'
LINK_IMGUR = 'imgur'
LINK_REDD = 'redd.it'
LINK_GYFCAT = 'gfycat'
RE_GC_LINK = r'<meta property="og:video:secure_url" content="(https:\/\/thcf.\.redgifs\.com\/[a-zA-Z]+\.mp4)">'
UA_FOR_GC = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'


def create_folder(sub):
    full_path = DUMP_PATH + 'r_' + sub
    if not os.path.exists(full_path):
        os.makedirs(full_path)


def dl_gc_link(score, author, link, sub):
    # link = re.search(RE_GF_LINK, url_source.read().decode())
    # print('...'.format(link))
    # print('dafuq')

    req = urllib.request.Request(
        link,
        headers={
            'User-Agent': UA_FOR_GC
        }
    )

    path = urlparse(link).path
    ext = os.path.splitext(path)[1]
    filename = '{}_{}{}'.format(score, author, ext)

    # download(req, filename, sub)

    fullpath = DUMP_PATH + 'r_' + sub + '/' + filename
    with urllib.request.urlopen(req) as response, open(fullpath,
                                                       'wb') as out_file:
        shutil.copyfileobj(response, out_file)


def dl_redd_imgur_link_rtn_fullpath(score, author, link, sub):
    path = urlparse(link).path

    ext = os.path.splitext(path)[1]

    # in the unlikely case that there is .gifv imgur file
    if ext == '.gifv':
        url = link.replace('gifv', 'mp4')
        ext = '.mp4'

        # Craft the filename for saving
        filename = '{}_{}{}'.format(score, author, ext)
    elif ext == '':
        url = link + '.jpg'

        print('this link unknown ext')
        print(link)
        print('----')

        # Craft the filename for saving
        filename = 'unknownfe_{}_{}{}'.format(score, author, ext)
    else:
        url = link
        # Craft the filename for saving
        filename = '{}_{}{}'.format(score, author, ext)

    return download_rtn_fullpath(url, filename, sub)


def download_rtn_fullpath(url, filename, sub, not_gc_or_imgur=1):
    fullpath = DUMP_PATH + 'r_' + sub + '/' + filename
    if not_gc_or_imgur:
        # start the download
        r = requests.get(url, allow_redirects=True)
        open(fullpath, 'wb').write(r.content)
        return fullpath
    else:
        pass


def convert_to_redgifs(link):
    res = requests.get(link, headers={'User-Agent': UA_FOR_GC})
    res_content = res.content.decode()
    redgif_link_groups = re.search(RE_GC_LINK, res_content)
    redgif_link = redgif_link_groups.group(1)
    return redgif_link


def preprocess_before_download_rtn_fullpath(score=0, author='', link='', sub=''):
    # create a folder to get ready for photo/video dump
    create_folder(sub)

    # if the links are imgur or redd.it
    if LINK_REDD in link or LINK_IMGUR in link:
        return dl_redd_imgur_link_rtn_fullpath(score, author, link, sub)

    # if the url is gyfcat
    elif LINK_GYFCAT in link:
        # link = convert_to_redgifs(link)
        # dl_gc_link(score, author, link, sub)
        print('[gyfcat] Going to next link instead.')


def main():
    number = randint(1111, 9999)
    preprocess_before_download_rtn_fullpath(number, 'chemicalJuice',
                               'https://gfycat.com/relievedsardonicasiaticmouflon',
                               'test')

    # preprocess_before_download(number, 'chemicalJuice',
    #                            'https://gfycat.com/SoreAmpleAntelope',
    #                            'test')


if __name__ == '__main__':
    main()
