# -*- coding: utf-8 -*-
# 多线程爬取

import os
import requests
import threading
from bs4 import BeautifulSoup



main_site = "http://society.people.com.cn"


# 获取页面中的所有新闻链接
def getUrl(text):
    ans = []
    soup = BeautifulSoup(text, 'lxml')
    a_tag_list = soup.find_all('a')
    for a_tag in a_tag_list:
        try:
            href = a_tag['href']
            if ("/n1/" in href) and ('http' not in href) and ("#liuyan" not in href):
                if href not in ans:
                    ans.append(href)
        except Exception as e:
            continue
    return ans


# 获取页面数据
# def getData(url, count, worksheet):
def getData(url):
    # 设置文本文档信息
    file_name = url.replace("/", "_")
    file_name += ".txt"
    file = open('./result/tmp_files/{}'.format(file_name), 'w', encoding="utf-8")

    # 爬取内容
    news_url = "http://society.people.com.cn" + url
    print("正在爬取：", news_url, "\n")
    res = requests.get(news_url)
    res.encoding = res.apparent_encoding
    #print(res.text)
    if res.status_code != 200:
        raise Exception("request error")

    # 消除html &nbsp编码
    soup = BeautifulSoup(res.text.replace("&nbsp;", " "), 'lxml')

    # 标题：news_title
    content_div = soup.find(name="div", attrs={"class": "layout rm_txt cf"}).find(name="div", attrs={"class": "col col-1 fl"})
    h1_tag = content_div.find(name="h1")
    news_title = h1_tag.text
    # 写入文档
    file.write("title ==> \n")
    file.write("\t\t{}".format(news_title))
    file.write("\n\n")

    # 时间：news_time
    time_div = soup.find(name="div", attrs={"class": "channel cf"}).find(name="div", attrs={"class": "col-1-1 fl"})
    news_time = time_div.text.replace("\n", "").replace(" ", "").replace("\t", "")
    # 写入文档
    file.write("time ==> \n")
    file.write("\t\t{}".format(news_time))
    file.write("\n\n")

    # 链接：news_url
    # 写入文档
    file.write("link ==> \n")
    file.write("\t\t{}".format(news_url))
    file.write("\n\n")

    # 内容：news_doc
    p_tag_list = soup.find_all(name="p", attrs={"style": "text-indent: 2em;"})
    file.write("content ==> \n")
    news_doc = ""
    for p_tag in p_tag_list:
        try:
            content = p_tag.text
            news_doc += content
            # 写入文档
            file.write(content + "\n")
        except Exception as e:
            print(url)
            print(e)


    # 图片：news_pic
    img_tag_list = soup.find_all(name="p", attrs={"style": "text-align: center;"})
    img_tag_list += soup.find_all(name="td", attrs={"style": "align: center"})
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
            # 写入文件
            img_file = open("./result/pics/{}".format(img_title), 'wb')
            img_file.write(img)
            img_file.close()
            exit()
        except Exception as e:
            continue

    # 关闭文档
    file.close()


# 创建文件夹
def newDir():
    if not os.path.exists("./result"):
        os.mkdir("./result")
    if not os.path.exists("./result/tmp_files"):
        os.mkdir("./result/tmp_files")
    if not os.path.exists("./result/pics"):
        os.mkdir("./result/pics")

# 主函数
def main():
    # 创建文件夹
    newDir()
    page_main_url = main_site + "/GB"
    url_list = []
    for i in range(1, 11):
        index = "/index" + str(i) + ".html"
        url = page_main_url + index
        res = requests.get(url)
        # 获取当前页面内部链接
        url_list += getUrl(res.text)
    # 链接去重
    url_list = list(set(url_list))
    print("--------------- START! ---------------")
    print("共有", len(url_list), "个新闻链接")
    #print(url_list)
    count = 1
    for news_url in url_list:
        try:
            threading.Thread(target=getData, args=(news_url,)).start()
        except Exception as e:
            continue
    print("---------------- END! ----------------")


if __name__ == '__main__':
    main()



