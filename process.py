import json 
import requests
from bs4 import BeautifulSoup

def load_json(filename):
    return json.load(open(filename, "r"))


def get_content_page(url, decode=True):
    r = requests.get(url)
    if r.status_code == 200:
        if decode:
            return r.content.decode("utf8")
        else:
            return r.content
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

def crawl_from_list_url():
    urls = load_json("./all_link.json")
    data = []
    for url in urls:
        tmp_data = {}
        tmp_data["url"] = url 
        content = get_content_page(url, decode=False)
        soup = BeautifulSoup(content, "html.parser")
        art = soup.find_all("article")[0]
        p = art.find_all("p", {"style": "font-size: 13px; font-family: Verdana"})[:-1]
        text = []
        for i in p:
            tmp = i.get_text(separator="<br>").strip().replace("<br>", "\n")
            tmp = tmp.split("\n")
            text += tmp
        tmp_data["paragraphs"] = text 
        data.append(tmp_data)
        print(url)
    with open("./data/add_data_1.json", "w", encoding="utf-8") as f:
        json.dump(data, f)

def process_data(data):
  new_data = []
  for para in data:
    para = [txt.strip() for txt in para]
    para = " . ".join(para)
    para = para.replace(",", " , ")
    while "  " in para:
      para = para.replace("  ", " ")
    while ". ." in para:
      para = para.replace(". .", ".")
    new_data.append(para)
  return new_data

if __name__ == "__main__":
    # run_crawl()
    # crawl_from_list_url()
    df1_root = json.load(open("./data/add_data.json", "r"))
    df2_root = json.load(open("./data/add_data_2.json", "r"))
    df3_root = json.load(open("./data/full_data.json", "r"))
    df1 = [" ".join(i["paragraphs"]) for i in df1_root]
    df1 = [[j.strip() + " ." for j in i.replace(".", " .").split(".") if len(j.strip())] for i in df1]
    print("df1:", len(df1))
    df2 = [" ".join(i["paragraphs"]) for i in df2_root]
    df2 = [[j.strip() + " ." for j in i.replace(".", " .").split(".") if len(j.strip())] for i in df2]
    print("df2:", len(df2))
    df3_tmp = list(df3_root.values())
    df3 = []
    for row in df3_tmp:
        df3 += row
    df3 = [" ".join(i["paragraphs"]) for i in df3]
    df3 = [[j.strip() + " ." for j in i.replace(".", " .").split(".") if len(j.strip())] for i in df3]
    print("df3:", len(df3))
    df = df1 + df2 + df3
    print("df:", len(df))
    data = process_data(df)
    with open("./data/dataset.json", "w", encoding="utf-8") as f:
        json.dump(data, f)