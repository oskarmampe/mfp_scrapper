from bs4 import BeautifulSoup
import requests
import re
import codecs
import os
import shutil

html = requests.get('https://musicforprogramming.net/latest')
soup = BeautifulSoup(html.text, features="html.parser")
links = soup.find(id="sapper").find_all(name="a")
for link in links:
    pattern = re.compile(r'/')
    linkText = link["href"]
    if not pattern.search(linkText):
        filePattern = re.compile(r'file:"(.*?)"', )
        path = os.path.join("{}.mp3".format(link.text))
        songUrl = 'https://musicforprogramming.net/{}'.format(linkText)
        newHtml = requests.get(songUrl)
        textHtml = BeautifulSoup(
            newHtml.text).find_all(name="script")[-1].text
        url = codecs.decode(filePattern.search(
            textHtml).group(1), 'unicode-escape')
        print(url)
        with requests.get(url, stream=True) as r:
            with open(path, 'wb') as f:
                shutil.copyfileobj(r.raw, f)
