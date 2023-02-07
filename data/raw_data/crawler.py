#Crawl data from this website https://www.ielts-mentor.com
import requests
import os
from bs4 import BeautifulSoup

#Get link
fhandle = open("ieltsmentor.json", "r")
all_links = fhandle.readlines()
fhandle.close()

#Get content from url and convert to txt file
f = open('DatafromIELTSmentor.txt', 'a')
def get_content(url, cnt):    
    url = url[3:len(url) - 3]
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    wrapper = soup.find('body')
    wrapper = wrapper.find_all('article', {"class": "item-page"})[0]
    #how to remove div card in wrapper html
    ftmp = open('tmp.txt', 'w') 
    for div in wrapper.find_all('div'):
        div.decompose()
    for dl in wrapper.find_all('dl'):
        dl.decompose()
    for ul in wrapper.find_all('ul'):
        ul.decompose()
    for li in wrapper.find_all('li'):
        li.decompose()
    for br in wrapper.find_all('br'):
        br.decompose()
    rwap = wrapper
    wrapper = wrapper.find('p')
    rwap = rwap.find_all('p')
    try:
        wrapper = wrapper.text
        ftmp.write(wrapper)
    except AttributeError:
        ftmp.write(str(wrapper))
    #gagfas
    ftmp = open('tmp.txt', 'r') 
    have = 0
    essay = []
    record = 0
    for line in ftmp.readlines():
        if line.startswith('	['):
            continue
        if (line.startswith("Model Answer") or line.startswith("Sample Answer") or line.startswith("Sample Essay") or line.startswith("Model Essay")):
            if record == 0:
                record = 1
        if record == 1 and line.startswith('	'):
            if line[2].isalpha():
                essay.append(line)
                have = 1
        elif (line.startswith("Model Answer") or line.startswith("Sample Answer") or line.startswith("Sample Essay") or line.startswith("Model Essay")):
            essay.append("*")
    ftmp.close()
    if have == 1:
        for line in essay:
            if line.startswith("*"):
                cnt += 1
                f.write(f"Essay {cnt}:\n")
            else:
                f.write(line)
    else:
        ftmp = open('tmp.txt', 'w') 
        for i in range(0, len(rwap)):
            try:
                wrapper = wrapper.text
                ftmp.write(wrapper)
            except AttributeError:
                ftmp.write(str(wrapper))
        ftmp = open('tmp.txt', 'r') 
        essay = []
        record = 0
        for line in ftmp.readlines():
            if line.startswith('	['):
                continue
            if (line.startswith("Model Answer") or line.startswith("Sample Answer") or line.startswith("Sample Essay") or line.startswith("Model Essay")):
                if record == 0:
                    record = 1
            if record == 1 and line.startswith('	'):
                if line[2].isalpha():
                    essay.append(line)
                    have = 1
            elif (line.startswith("Model Answer") or line.startswith("Sample Answer") or line.startswith("Sample Essay") or line.startswith("Model Essay")):
                essay.append("*")
        ftmp.close()
        for line in essay:
            if line.startswith("*"):
                cnt += 1
                f.write(f"Essay {cnt}:\n")
            else:
                f.write(line)
    return cnt

cnt = 0
for i in range(1, len(all_links) - 1):
    f.write("Link:" + str(all_links[i]))
    cnt = get_content(all_links[i], cnt)
f.close()


