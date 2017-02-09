import re
import requests
import youtube_dl

from bs4 import BeautifulSoup


def find_search_content(search):
    request = requests.get("https://www.youtube.com/results?search_query={}".format(search))
    content = request.content
    soup = BeautifulSoup(content, "html.parser")
    return soup

def find_page_content(search):
    request = requests.get("https://www.youtube.com/results?{}".format(search))
    content = request.content
    soup = BeautifulSoup(content, "html.parser")
    return soup




def find_video(soup, all_item, i=1):
    all_item = {}
    for element in soup.find_all('a',{"rel": "spf-prefetch"}):
        title = element.get('title')
        link = element.get('href')
        img_link = element.get('href').split('=')[1]
        img = soup.find_all('img', {"height": True})
        img2 = str(re.findall("https://i.ytimg.com/vi/{}/[\S]+".format(img_link), str(img))).strip("[\'\"\]")
        img2 = img2.replace("&amp;", "&")
        all_item['{}'.format(i)] = {"title": title, "link" : "https://www.youtube.com{}".format(link),
                                    "image": img2}
        i=i+1
    return all_item


def video_time(soup, all_item, i=1):
    for time in soup.find_all("span", {"class": "video-time"}):
        all_item.get('{}'.format(i))['time']=time.text
        i=i+1

    return all_item


def every_video(soup):
    all_item = {}
    find_video(soup, all_item, i=1)
    video_time(soup, all_item, i=1)
    return all_item


def page_bar(soup):
    page = {}
    for page_value in soup.find_all('a',
                                    {"aria-label": True, "data-sessionlink": True, "data-visibility-tracking": True}):
        page1 = page_value.get("href")
    #    video_page = "https://www.youtube.com/{}".format(page1)
        page['{}'.format(page_value.text)] = page1

    return page


def download_mp3(url):
    ydl_opts = {'format': 'bestaudio/best', 'outtmpl': 'Video/%(title)s.%(ext)s',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }]}

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


def download_mp4(url):
    ydl_opts = {'format': 'best','outtmpl': 'Video/%(title)s.%(ext)s'}

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])








