'''
This script fetches a rss-feed, downloads images contained in it to a local directory
and writes a new feed-file that serves the images from the local directory.
'''
import urllib.request
import feedparser
import fileinput
from bs4 import BeautifulSoup

original_feed = 'https://somehost/somedir/feed'
urllib.request.urlretrieve(original_feed, 'tempdir' + '/feed.xml')

local_prefix = 'https://yourhost/somedir/'
d = feedparser.parse(original_feed)

images = []

# find url of images and fetch them to local dir
for item in d['entries']:
    soup = BeautifulSoup(item['summary'], 'html.parser')
    img = soup.select('img')
    images = [i['src'] for i in img if  i['src']]
    for image in images:
        localfile = 'tempdir/' + image.split('/')[-2] + '_' + image.split('/')[-1]
        newurl = str(local_prefix) + str(localfile)
        # print('saving ' + str(image) + ' to ' + str(localfile))
        urllib.request.urlretrieve(image, localfile)
        # and now we search and replace in the file...
        # instead of importing a library to generate rss-feeds...
        with fileinput.FileInput('tempdir/feed.xml', inplace=True, backup='.bak') as file:
            for line in file:
            print(line.replace(image, newurl), end='')
