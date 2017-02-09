import re

import requests
from bs4 import BeautifulSoup

request = requests.get("https://www.youtube.com/results?search_query=pitbull")
content = request.content
soup = BeautifulSoup(content, "html.parser")

page={}

for page_value in soup.find_all('a',{"aria-label":True, "data-sessionlink":True, "data-visibility-tracking":True}):
    page1 = page_value.get("href")
    video_page = "https://www.youtube.com/{}".format(page1)
    page['{}'.format(page_value.text)]= page1

print(page)