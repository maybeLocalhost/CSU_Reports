import scrapy


class SocietyPeopleSpider(scrapy.Spider):
    name = 'society_people'
    allowed_domains = ['society.people.com.cn']
    start_urls = ['http://society.people.com.cn/']

    def parse(self, response):
        # print(response.text)
        news_title = response.xpath("//div[@class='hdNews clearfix']/div[@class='on']/h5/a").extract()
        test = []
        for news_title in zip(news_title):
            test.append({'news_title': news_title})
        print(len(test))
        return test

