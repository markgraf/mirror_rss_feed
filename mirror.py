'''
This script fetches a rss-feed, downloads images contained in it to a local directory
and writes a new feed-file that serves the images from the local directory.

Useful to embed e.g. an ebay-feed into your site without forwarding your users
IP-adress to ebay...
'''
import codecs
import urllib.request
import feedparser
from bs4 import BeautifulSoup

d = feedparser.parse('https://some_feed_you_want_to_mirror/feed')
f = str(d)
images = []

# find url of images
for item in d['entries']:
    soup = BeautifulSoup(item['summary'], 'html.parser')
    img = soup.select('img')
    images.extend([i['src'] for i in img if  i['src']])

# download file to temp-dir
for image in images:
    localfile = 'tempdir/' + image.split('/')[-2] + '_' + image.split('/')[-1]
    #print('saving ' + str(image) + ' to ' + str(localfile))
    urllib.request.urlretrieve(image, localfile)
    # rewrite the original feed to use local files
    f = f.replace(str(image), str(localfile))

outfile = codecs.open('new_feed.rss', 'w', 'utf-8')
outfile.write(f)
outfile.close()
