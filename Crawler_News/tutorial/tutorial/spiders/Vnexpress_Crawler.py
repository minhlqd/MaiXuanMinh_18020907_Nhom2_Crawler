import json

import scrapy
from datetime import datetime

OUTPUT = 'J:/PycharmProject/Crawler_News/tutorial/tutorial/spiders/output/vnexpress/vnexpress_{}.txt'.format(datetime.now().strftime('%Y%m%d_%H%M%S'))

class Vnexpress_Crawler(scrapy.Spider):
    name = 'vnexpress_crawler'
    allowed_domains = ['vnexpress.net']
    start_urls = ['https://vnexpress.net']
    count = 0

    def parse(self, response):
        if response.status == 200 and response.css('meta[name="tt_page_type"]::attr("content")').get() == 'article':
            print('Crawling from: ' + response.url)
            data = {
                'Link': response.url,
                'Title': response.css('h1.title-detail::text').get(),
                'Description': response .css('p.description::text').get(),
                'Content': '\n'.join([
                    ''.join(crawl.css('*::text').getall())
                    for crawl in response.css('article.fck_detail p.Normal')
                ]),
                'Category': response.css('ul.breadcrumb > li > a::attr("title")').get(),
                'Date': response.css('span.date::text').get(),
                'Tags': response.css('meta[name="its_tag"]::attr("content")').get()
            }
            with open(OUTPUT, 'a', encoding='utf8') as f:
                f.write(json.dumps(data, ensure_ascii=False))
                f.write('\n')
                self.count += 1
                self.crawler.stats.set_value('Count', self.count)
                print(self.count)
                print('SUCCESS:', response.url)

        for i in response.css('a[href^="https://vnexpress.net"]::attr(href)').getall():
            yield scrapy.Request(i, callback=self.parse)

#        yield from response.follow_all(css='a[href^="https://vnexpress.net"]::attr(href), a[href^="/"]::attr(href)',
#                                       callback=self.parse)









