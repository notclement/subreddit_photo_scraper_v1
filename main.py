"""
Written by: Clement
"""

import sys
import praw
from osxmetadata import OSXMetaData

from private.secrets import *
from file_download import preprocess_before_download_rtn_fullpath

DUMP_PATH = './dump/'
SORT_TYPES = ['top', 'best', 'new', 'controversial', 'hot', 'rising']
UA = 'testscript by /u/iobdug'


class Submission:
    def __init__(self, title, author, score, url, is_self, permalink):
        self.title = title
        self.author = author
        self.score = score
        self.url = url
        self.is_self = is_self
        self.permalink = permalink

    def add_meta_info(self, path_to_image):
        # obj to manipulate the metadata
        if path_to_image is not None:
            meta = OSXMetaData(path_to_image)

            # set description
            meta.append_attribute('findercomment',
                                  '{}\n{}\n{}\n{}\n{}'.format(
                                      self.title,
                                      self.author,
                                      self.score,
                                      'www.reddit.com' + self.permalink,
                                      self.url
                                  ))


def get_subreddit_sort_by(subreddit, sort_by, limit):
    if sort_by == 'top':
        return subreddit.top(time_filter='all', limit=limit)
    elif sort_by == 'best':
        return subreddit.best(time_filter='all', limit=limit)
    elif sort_by == 'hot':
        return subreddit.hot(time_filter='all', limit=limit)
    elif sort_by == 'new':
        return subreddit.new(time_filter='all', limit=limit)
    elif sort_by == 'controversial':
        return subreddit.controversial(time_filter='all', limit=limit)
    elif sort_by == 'rising':
        return subreddit.rising(time_filter='all', limit=limit)


def get_reddit_obj():
    return praw.Reddit(client_id=client_id,
                       client_secret=client_secret,
                       user_agent=UA,
                       username=account_id,
                       password=account_pw)


def get_params():
    # if len(sys.argv) == 4:
    #     sub = sys.argv[1]
    #     if sys.argv[2] in SORT_TYPES:
    #         sort_by = sys.argv[2]
    #     else:
    #         print('Error. Please choose correct sort type.')
    #         for i in SORT_TYPES:
    #             print(i)
    #         sys.exit(1)
    #     try:
    #         limit = int(sys.argv[3])
    #     except TypeError:
    #         print('Error. Supply only integers for the limit')
    #         sys.exit(1)
    #
    #     return sub, sort_by, limit
    # else:
    #     print('USAGE: main.py <sub> <sort_type> <limit>')

    sub = sys.argv[1]
    sort_by = sys.argv[2]
    limit = int(sys.argv[3])

    return sub, sort_by, limit


def main():
    sub, sort_by, limit = get_params()

    # Get the reddit object in order to call its methods
    reddit = get_reddit_obj()

    # select the subreddit we want to interact with
    subreddit = reddit.subreddit(sub)

    # filter what kind of post we want from that subreddit
    subreddit = get_subreddit_sort_by(subreddit, sort_by, limit)

    num_of_submissions = 0
    dict_name = {}
    for submission in subreddit:
        if reddit.auth.limits['remaining'] != 0:
            result = "result{0}".format(num_of_submissions)
            dict_name[result] = Submission(submission.title,
                                           submission.author,
                                           submission.score,
                                           submission.url,
                                           submission.is_self,
                                           submission.permalink)

            full_path = preprocess_before_download_rtn_fullpath(
                submission.score,
                submission.author,
                submission.url,
                sub)

            # # set meta data info
            dict_name[result].add_meta_info(full_path)

            num_of_submissions += 1
        else:
            print('Request limit reached.')
            sys.exit(1)


if __name__ == '__main__':
    main()
