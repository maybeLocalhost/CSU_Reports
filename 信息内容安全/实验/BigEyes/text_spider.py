# -*- coding: utf-8 -*-

import os
import requests
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
def getData(url, file):

    # 爬取内容
    news_url = "http://society.people.com.cn" + url
    print("正在爬取：", news_url)
    res = requests.get(news_url)
    res.encoding = res.apparent_encoding
    if res.status_code != 200:
        raise Exception("request error")

    # 消除html &nbsp编码
    soup = BeautifulSoup(res.text.replace("&nbsp;", " "), 'lxml')

    # 标题：news_title
    content_div = soup.find(name="div", attrs={"class": "layout rm_txt cf"}).find(name="div", attrs={"class": "col col-1 fl"})
    h1_tag = content_div.find(name="h1")
    news_title = h1_tag.text
    # 写入文档
    file.write(news_title.replace(" ", "").replace("\n","").replace("\t",""))

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
            content = p_tag.text
            news_doc += content
            # 写入文档
            file.write(content.replace(" ", "").replace("\n","").replace("\t",""))
        except Exception as e:
            print(url)
            print(e)


# 主函数
def main():
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
    count = 1
    file = open('feel/news.txt', 'a+', encoding='utf-8')
    for news_url in url_list:
        try:
            getData(news_url, file)
            count += 1
            # # 数量控制
            # if count == 6:
            #     break
        except Exception as e:
            continue
    # 关闭文档
    file.close()
    print("---------------- END! ----------------")

if __name__ == '__main__':
    main()



