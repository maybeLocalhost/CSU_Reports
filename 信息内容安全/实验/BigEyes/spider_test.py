import os
import sys
import threading

import requests
from bs4 import BeautifulSoup

main_site = "http://society.people.com.cn"


def get_page_list(text: str) -> list:
    ans = []
    class_name = "page_n clearfix"
    soup = BeautifulSoup(text, 'lxml')
    page_tag = soup.find(name="div", attrs={"class": class_name})
    # print(page_tag)
    page_link_list = page_tag.find_all("a")
    for page_link in page_link_list:
        try:
            href = page_link['href']
            if href not in ans:
                ans.append(page_link['href'])
        except Exception as e:
            continue
    return ans


def get_insite_url_link(text: str) -> list:
    ans = []
    soup = BeautifulSoup(text, 'lxml')
    a_tag_list = soup.find_all('a')
    for a_tag in a_tag_list:
        try:
            href = a_tag['href']
            if ("/n1/" in href) and ('http' not in href) and ("#liuyan" not in href):
                if href not in ans:
                    ans.append(href)
            pass
        except Exception as e:
            continue
    return ans


def get_content_from_url(url: str) -> None:
    file_name = url[7:].replace("/", "_")
    file_name += ".txt"
    file = open('./tmp_files/{}'.format(file_name), 'w', encoding="utf-8")
    res = requests.get(url=url)
    res.encoding = res.apparent_encoding
    # print(res.text)
    if res.status_code != 200:
        raise Exception("request error")

    # 消除html &nbsp编码
    soup = BeautifulSoup(res.text.replace("&nbsp;", " "), 'lxml')

    # 找到标题
    file.write("title ==> \n")
    content_div = soup.find(name="div", attrs={"class": "layout rm_txt cf"}).find(name="div",
                                                                                  attrs={"class": "col col-1 fl"})
    h1_tag = content_div.find(name="h1")
    title = h1_tag.text
    file.write("\t\t{}".format(title))
    file.write("\n\n")

    # 链接
    file.write("link ==> \n")
    file.write("\t\t{}".format(url))
    file.write("\n\n")

    # 找到时间
    file.write("time ==> \n")
    time_div = soup.find(name="div", attrs={"class": "channel cf"}).find(name="div", attrs={"class": "col-1-1 fl"})
    content_time = time_div.text.replace("\n", "").replace(" ", "").replace("\t", "")
    file.write("\t\t{}".format(content_time))
    file.write("\n\n")

    # 找到内容
    file.write("content ==> \n")
    p_tag_list = soup.find_all(name="p", attrs={"style": "text-indent: 2em;"})
    for p_tag in p_tag_list:
        try:
            content = p_tag.text
            file.write(content + "\n")
        except Exception as e:
            print(url)
            print(e)

    # 找到图片
    img_tag_list = []
    img_tag_list = soup.find_all(name="p", attrs={"style": "text-align: center;"})
    if len(img_tag_list) == 0:
        file.close()
        return None
    for img_tag in img_tag_list:
        try:
            img_src = img_tag.find(name="img")['src']
            img_url = main_site + img_src
            img_title = img_url[7:].replace("/", "_")
            res = requests.get(img_url)
            img = res.content
            img_file = open("./pics/{}".format(img_title), 'wb')
            img_file.write(img)
            img_file.close()
        except Exception as e:
            continue

    file.close()
    pass


def init():
    if not os.path.exists("./tmp_files"):
        os.mkdir("./tmp_files")
    if not os.path.exists("./pics"):
        os.mkdir("./pics")


def main():
    init()

    page_main_url = main_site + "/GB"
    index1 = "/index1.html"
    url1 = page_main_url + index1
    res = requests.get(url=url1)
    page_list = get_page_list(res.text)
    insite_url_list = []
    for page in page_list:
        page_url = page_main_url + "/" + page
        res = requests.get(page_url)
        insite_url_list += get_insite_url_link(res.text)

    # 去重
    insite_url_list = list(set(insite_url_list))
    print("start ==> {}".format(len(insite_url_list)))
    i = 0
    for url in insite_url_list:
        i += 1
        content_url = main_site + url
        try:
            #get_content_from_url(content_url)
            threading.Thread(target=get_content_from_url, args=(content_url,)).start()
        except Exception as e:
            continue
    print("ends ==> {}".format(i))


if __name__ == '__main__':
    main()
