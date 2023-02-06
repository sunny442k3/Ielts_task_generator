

import requests
from bs4 import BeautifulSoup

url = 'https://www.ielts-mentor.com/writing-sample/writing-task-2'
links = []
for idx in range(0, 1240, 20):
    if idx == 0:
        new_url = url 
    else:
        new_url = url + "?start=" + str(idx)
    links.append(new_url)
    break
    

def get_content(url):
    r = requests.get(url)
    return r.content 

content = get_content(links[0])
print(content)
# response = requests.get(url)
# soup = BeautifulSoup(response.text, 'html.parser')

# # Find the main content of the page 
# main_content = soup.find('div', class_='post_content') 
# # Find all the paragraphs in the main content 
# paragraphs = main_content.find_all('p') 
# # Iterate over each paragraph and print its text 
# for p in paragraphs: 
#     print(p.text)