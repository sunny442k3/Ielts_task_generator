import json 
import requests
from bs4 import BeautifulSoup

def load_json(filename):
    return json.load(open(filename, "r"))


def get_content_page(url):
    r = requests.get(url)
    if r.status_code == 200:
        return r.content.decode("utf8")
    return ""


def get_paragraph(content):
    soup = BeautifulSoup(content, "html.parser")
    div = soup.find_all("div", {"class": "vocab-paragraphs"})[0]
    para = div.find_all("div", {"class": "vocab-idea-wrapper"})
    para = [
        tmp.find_all("div", {"class": "text"}) for tmp in para
    ]
    paragraphs = []
    for i in range(len(para)):
        paragraphs.append(para[i][0].text.strip(" "))
    return paragraphs


def run_crawl():
    data = load_json("./process_data.json")
    new_data = {}
    count = 0
    inc = []
    for k, v in data.items():
        if k not in new_data:
            new_data[k] = []
        for idx, row in enumerate(v):
            try:
                content = get_content_page(row["url"])
                if len(content) == 0:
                    inc += [count]
                    count += 1
                    continue
                count += 1
                paragraphs = get_paragraph(content)
                row["paragraphs"] = paragraphs
                new_data[k].append(row)
                print(f"[{count}]", row["url"])
            except:
                with open("./full_data.json", "w", encoding="utf-8") as f:
                    json.dump(new_data, f)
    with open("./full_data.json", "w", encoding="utf-8") as f:
        json.dump(new_data, f)

if __name__ == "__main__":
    run_crawl()