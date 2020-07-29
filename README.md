# subreddit_photo_scraper_v1

This program will scrape images off a chosen subreddit.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 

```
Tested and working with imgur and redd.it links so far.
```

### Prerequisites

Use the provided requirements.txt to get the needed libraries installed

```
pip3 install -r requirements.txt
```

### Installing

Steps on getting it working

```
1. Create a .py file in private named secrets.py
2. In it, add the following
    - 'account_id' : Reddit account ID
    - 'account_pw' : Reddit account password
    - 'client_id' : client id for reddit api
    - 'client_secret' : client secret for reddit api

You can get your reddit API creds here: https://www.reddit.com/prefs/apps
```

## Running the script

```\
Once you have got all of that done, you can just run the following command

> python3 main.py <sub> <sorted_by> <limit>

e.g. `main.py aww top 500` 

Sorted by - top, best, hot, new, rising, controversial
```

## Learning objectives

```
1. Making use of classes
2. Learn how to use PRAW (Python Reddit API Wrapper)
```

## Some comments

```
The code is really messy especially in `file_download.py` as i tried doing gfycat downloads and had error requesting resources too many time in a short period of time.

I also didn't complete the parameter check for the script.

Also, I would love some feedback on my use of classes in `main.py` as it is my first time utilising classes, I am still learning if my way of generating variables with dictionaries is good or bad.
```