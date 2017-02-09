import re

import requests
from bs4 import BeautifulSoup

request = requests.get("https://www.youtube.com/results?search_query=pitbull")
content = request.content
soup = BeautifulSoup(content, "html.parser")

for element in soup.find_all('a',{"rel": "spf-prefetch"}):
    video_link = element.get('href').split('=')[1]
    img = soup.find_all('img',{"height":True})
    img2 = str(re.findall("https://i.ytimg.com/vi/{}/[\S]+".format(video_link),str(img))).strip("[\'\"\]")
    img2 = img2.replace("&amp;","&")
    print(img2)



