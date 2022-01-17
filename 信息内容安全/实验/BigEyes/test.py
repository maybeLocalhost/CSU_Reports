# -*- coding: utf-8 -*-

import re

import requests
from bs4 import BeautifulSoup


main_site = "http://society.people.com.cn"

# 获取页面数据
def getData(url):

    # 爬取内容
    news_url = url
    print("正在爬取：", news_url)
    res = requests.get(news_url)
    res.encoding = res.apparent_encoding
    if res.status_code != 200:
        raise Exception("request error")

    # 消除html &nbsp编码
    soup = BeautifulSoup(res.text.replace("&nbsp;", " "), 'lxml')

    # 内容：news_doc
    # test = soup.find(name="div", attrs={"class": "rm_txt_con cf"}).find(name='p')
    # print(test)

    # for item in soup.find_all(name="div", attrs={"class": "rm_txt_con cf"}):
    #     if item.find(name='table'):
    #         item.table.decompose()
    #
    #     test = item.find_all(name='p', attrs={"class": ""})
    #     print(test)
    #     print("\n\n\n")
    #     for p in test:
    #         if p.find(name='span', attrs={"id": "paper_num"}):
    #             continue
    #         else:
    #             c = p.text
    #             print(c)




    # findDoc = re.compile(r"<p>(.*?)</p>")
    # for item in soup.find_all(name="div", attrs={"class": "rm_txt_con cf"}):
        # item = str(item)
        # print(item)
        # doc = re.findall(findDoc, item)
        # print(doc)

    # p_tag_list = soup.find_all(name="p", attrs={"style": "text-indent: 2em;"})
    # if len(p_tag_list) == 0:
    #     p_tag_list = soup.find_all(name='p', attrs={"style": "text-indent: 2em"})
    #     if len(p_tag_list) == 0:
    #         test = soup.find(name="div", attrs={"class": "rm_txt_con cf"})
    #         print(test)
    #     #     if len(p_tag_list) == 0:
    #     #         p_tag_list = soup.find(name="div", attrs={"class": "rm_txt_con cf"}).find(name="span", attrs={"id": "paper_num"})

# 图片：news_pic
    img_tag_list = []
    for img_item in soup.find_all(name="div", attrs={"class": "rm_txt_con cf"}):
        img_tag_list += img_item.find_all(name="p", attrs={"style": "text-align: center;"})
        img_tag_list += img_item.find_all(name="td", attrs={"style": "align: center"})
        img_tag_list += img_item.find_all(name="p", attrs={"style": "text-align:center;"})
        img_tag_list += img_item.find_all(name="td", attrs={"style": "align:center"})

    print(img_tag_list)
    if len(img_tag_list) == 0:
        return None
    for img_tag in img_tag_list:
        try:
            img_src = img_tag.find(name="img")['src']
            print(img_src + "\n")
            if img_src == "/img/next_page.jpg" or img_src == "/img/prev_page.jpg":
                continue
            # img_url = main_site + img_src
            # img_title = img_url[7:].replace("/", "_")
            # res = requests.get(img_url)
            # img = res.content
            # # 写入文件
            # img_file = open("./result/pics/{}".format(img_title), 'wb')
            # img_file.write(img)
            # img_file.close()
            # # exit()
        except Exception as e:
            continue

# 主函数
def main():
    print("--------------- START! ---------------")
    # news_url = "http://society.people.com.cn/n1/2020/0423/c1008-31684251.html"
    # news_url = "http://society.people.com.cn/n1/2021/0526/c1008-32113708-2.html"
    news_url = "http://society.people.com.cn/n1/2021/0520/c1008-32108904.html"
    getData(news_url)
    print("---------------- END! ----------------")


if __name__ == '__main__':
    main()