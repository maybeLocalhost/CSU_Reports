# -*- coding: utf-8 -*-

import os
import requests
import csv
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
def getData(url, f_csv):
    # 爬取内容
    news_url = "http://society.people.com.cn" + url
    print("正在爬取：", news_url)
    res = requests.get(news_url)
    res.encoding = res.apparent_encoding
    if res.status_code != 200:
        raise Exception("request error")

    # 消除html &nbsp编码
    soup = BeautifulSoup(res.text.replace("&nbsp;", " "), 'lxml')

    # 信息列表
    news_data = []

    # 标题：news_title
    content_div = soup.find(name="div", attrs={"class": "layout rm_txt cf"}).find(name="div", attrs={"class": "col col-1 fl"})
    h1_tag = content_div.find(name="h1")
    news_title = h1_tag.text
    news_data += news_title


    # 时间：news_time
    time_div = soup.find(name="div", attrs={"class": "channel cf"}).find(name="div", attrs={"class": "col-1-1 fl"})
    news_time = time_div.text.replace("\n", "").replace(" ", "").replace("\t", "")
    news_data += news_time


    # 链接：news_url
    news_data += news_url


    # 内容：news_doc
    doc_list = []
    for doc_item in soup.find_all(name="div", attrs={"class": "rm_txt_con cf"}):
        if doc_item.find_all(name='table'):
            doc_item.table.decompose()
        doc_list += doc_item.find_all(name="p", attrs={"style": "text-indent: 2em;"})
        if len(doc_list) == 0:
            doc_list += doc_item.find_all(name='p', attrs={"style": "text-indent: 2em"})
            if len(doc_list) == 0:
                doc_list += doc_item.find_all(name='p', attrs={"class": ""})
    news_doc = ""
    for p_tag in doc_list:
        try:
            if p_tag.find(name='span', attrs={"id": "paper_num"}):
                continue
            news_doc += p_tag.text
        except Exception as e:
            print(url)
            print(e)
    news_data += news_doc


    # 图片：img_url
    img_tag_list = []
    for img_item in soup.find_all(name="div", attrs={"class": "rm_txt_con cf"}):
        img_tag_list += img_item.find_all(name="p", attrs={"style": "text-align: center;"})
        img_tag_list += img_item.find_all(name="td", attrs={"style": "align: center"})
        img_tag_list += img_item.find_all(name="p", attrs={"style": "text-align:center;"})
        img_tag_list += img_item.find_all(name="td", attrs={"style": "align:center"})
    if len(img_tag_list) == 0:
        return None
    img_xls = ""
    for img_tag in img_tag_list:
        try:
            img_src = img_tag.find(name="img")['src']
            if img_src == "/img/next_page.jpg" or img_src == "/img/prev_page.jpg":
                continue
            img_url = main_site + img_src
        except Exception as e:
            continue

    # 写入CSV文件
    f_csv.writerow[news_data]


# 主函数
def main():
    # 创建或打开一个CSV文件
    headers = ['title', 'time', 'url', 'doc'] # 标题、时间、链接、内容
    with open('data.csv', 'w', newline='') as f:
        f_csv = csv.writer(f)
        f_csv.writerow(headers)

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
            getData(news_url, f_csv)
            count += 1
            # 数量控制
            if count == 11:
                break
        except Exception as e:
            continue
    f.close()
    print("---------------- END! ----------------")

if __name__ == '__main__':
    main()



