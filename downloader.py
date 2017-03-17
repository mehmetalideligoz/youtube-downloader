# coding=utf-8
__author__ = '_raist'

import re
import urllib2
from urlparse import parse_qs
import Queue
import threading
import time
import sys

def download(video_url):

    # returns the video id
    video_id = video_url.split("watch?v=")[1]
    get_info_url = "http://www.youtube.com/get_video_info?video_id=" + video_id

    # read the metadata
    video_info = parse_qs(urllib2.urlopen(get_info_url).read())

    if video_info["status"][0] == 'fail':
        print "Error Code: ", video_info["errorcode"]
        print video_info["reason"][0].decode('utf-8')
        return None

    title = video_info['title'][0].decode('utf-8')

    # different resolutions and codecs in url_maps
    url_encoded_fmt_stream_map = video_info['url_encoded_fmt_stream_map'][0].split(',')

    entries = []
    for entry in url_encoded_fmt_stream_map:
        entries.append(parse_qs(entry))

    # Todo: Quality Option
    urls = []
    for entry in entries:
        #print entry
        urls.append(entry['url'][0])

    file_name = re.sub('[!@#$/]', '', title) + ".mp4"

    for key, val in video_info.iteritems():
        line = str(key), ": ", str(val)
        #print line

    print file_name + " is downloading now..."

    # Get the direct youtube link
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': '*/*',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'gzip, deflate, sdch, br',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive',
        'Origin':'https://www.youtube.com',
           'X-Client-Data':'CJO2yQEIpLbJAQjEtskBCIqSygEI+5zKAQipncoB'}

    # Write to the file

    request = urllib2.Request(urls[0], headers= hdr)
    print urls[2];
    try:
        page = urllib2.urlopen(request)
    except urllib2.HTTPError, e:
        print e.fp.read()

    page = urllib2.urlopen(request)
    CONTENT_LENGTH = int(page.headers['content-length'])/(1024*1024)
    CHUNK = 3 * 1024 * 1024
    processed_so_far = 3
    with open(file_name, 'ab+') as fp:
      while True:
        sys.stdout.write("\r" + str(processed_so_far) + "/" + str(CONTENT_LENGTH))
        sys.stdout.flush()
        #print "Status: " + str(processed_so_far) + "/" + str(CONTENT_LENGTH) + " MB" + "\r"
        chunk = page.read(CHUNK)
        if not chunk:
            break
        fp.write(chunk)
        processed_so_far += 3


def main():
    # sample: https://www.youtube.com/watch?v=5-sfG8BV8wU
    # sample2: https://www.youtube.com/watch?v=5WVamWiKuJw
    video_url = raw_input("Enter a youtube url: ")


    download(video_url)
    print "Done!"

if __name__ == '__main__':
    main()
