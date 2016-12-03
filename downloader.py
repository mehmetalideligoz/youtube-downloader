# coding=utf-8
__author__ = '_raist'
import time
import re
import urllib2
from urlparse import parse_qs
import os

def download(video_url, video_quality):

    # VERY_LOW_QUALITY = 5
    # LOW_QUALITY = 4
    # MEDIUM_QUALITY = 3
    # MEDIUM_HIGH_QUALITY = 2
    # HIGH_QUALITY = 1
    # VERY_HIGH_QUALITY = 0

    # Return video_id 
    video_url = video_url.split("&")[0]
    video_id = video_url.split("watch?v=")[1]
    get_info_url = "http://www.youtube.com/get_video_info?video_id=" + video_id

    #video_info contains; author, viewers, video's picture etc.
    #use parse_qs to split titles and data
    video_info = parse_qs(urllib2.urlopen(get_info_url).read())

    #.decode('utf-8') will prevent "non ascii charcter..." errors.
    title = video_info['title'][0].decode('utf-8')

    #different resolutions and codecs in url_maps
    url_encoded_fmt_stream_map = video_info['url_encoded_fmt_stream_map'][0].split(',')

    entries = []
    for entry in url_encoded_fmt_stream_map:
        entries.append(parse_qs(entry))

    # TODO: user should select a resolution
    urls = []
    for entry in entries:
        urls.append(entry['url'][0]) # for now, user selects the best resolution


    # Title may contain special characters that cannot be in the filename, so remove them.
    # TODO: Instead of adding .mp4 at the end, parse the container type of the video
    file_name = re.sub('[!@#$/]', '', title) + ".mp4"
    directory = "C:/Downloads/YoutubeVideos/"
    
    dir = os.path.dirname(directory)

    if not os.path.exists(directory):
        os.makedirs(directory)
    
    
    print file_name + " is downloading now..."


    #get the url (I selected the first url by calling url_maps[0]['url'], improve this part of code) and write to file
    request = urllib2.Request(urls[video_quality])
    file = open(directory + file_name, 'wb')
    buffer = urllib2.urlopen(request).read()
    file.write(buffer)
    file.close()

    return True

# TODO: Instead of returning true or false, return the get_info file so that you don't have to do the same thing twice!
def check_url(video_url):

    if "www.youtube.com/watch?v=" not in video_url:
        return False

    video_url= video_url.split("&")[0]
    video_id = video_url.split("watch?v=")[1]
    get_info_url = "http://www.youtube.com/get_video_info?video_id=" + video_id

    #video_info contains; autbor, viewers, video's picture etc.
    #use parse_qs to split titles and data
    video_info = parse_qs(urllib2.urlopen(get_info_url).read())

    if video_info['status'][0] == 'fail':
        print video_info['status'][0]
        return False

    return True

def get_video_quality():

    video_quality = raw_input ("""
    VERY_LOW_QUALITY = 5
    ...
    VERY_HIGH_QUALITY = 0

    Select the video quality [0-5]:
    """)

    video_quality = int(video_quality)

    if (video_quality < 0) and (video_quality > 5):
        print "Enter a valid number between [0-5]"
        return get_video_quality()

    return video_quality


def main():
    print "Youtube Downloader v1.0 by _raist"
    print "This version downloads only one type of the video (720p), so if your internet connection is poor geçmiş olsun."
    print "The part after watch?v= is defined as video ID, for example if URL is https://www.youtube.com/watch?v=0CS2bwTw0Jg, the ID is VAnv66NDZ74"
    print "------------------------------------------------------------------------------------------------------------------------------------------"

    video_url = str(raw_input("Enter the video URL: "))

    while not check_url(video_url):
        print "Please enter a valid youtube URL... For example: 'https://www.youtube.com/watch?v=VAnv66NDZ74'"
        video_url = str(raw_input("Enter the video URL: "))


    video_quality = get_video_quality()

    start_time = time.time()
    download(video_url, video_quality)
    elapsed_time = time.time() - start_time

    print "Downloaded in " + str(elapsed_time) + " seconds."

    print "File is under C:/Downloads/Youtube Downloader directory."

if __name__ == '__main__':
    main()
