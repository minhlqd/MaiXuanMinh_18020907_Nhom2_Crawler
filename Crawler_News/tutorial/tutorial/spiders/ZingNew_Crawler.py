import json

import scrapy
from datetime import datetime

f = 'J:/PycharmProject/Crawler_News/tutorial/tutorial/spiders/output/ZingNew/ZingNew_{}.txt'.format(
    datetime.now().strftime('%Y%m%d_%H%M%S'))


class ZingNew_Crawler(scrapy.Spider):
    name = 'ZingNew_crawler'
    allowed_domains = ['zingnews.vn']
    start_urls = ['https://zingnews.vn']
    count = 0

    def parse(self, response):
        if response.status == 200 and response.css('meta[property="og:type"]::attr("content")').get() == 'article':
            print('Crawling from: ' + response.url)
            data = {
                'Link': response.url,

                'Title': response.css('h1.the-article-title::text').get(),

                'description': response.css('section.main  p.the-article-summary::text').get(),

                'content': '\n'.join([
                    ''.join(c.css('p::text').getall())
                    for c in (response.css('section.main > div.the-article-body > p'))
                ]),
                #            author = response.css('ul.the-article-meta li.the-article-author a::text').get()
                #            f.write('Author: ' + author + '  ')

                'date': response.css('ul.the-article-meta li.the-article-publish::text').get()

                #            tags = response.css('meta[property="article:tag"]::attr("content")').getall().split(',')
                #            f.write('Tag: ' + tags + '\n' + "\n")

            }
            with open(f, 'a', encoding='utf8'):
                f.write(json.dumps(data, ensure_ascii=False))
                f.write('\n')
                self.count += 1
                self.crawler.stats.set_value('Count', self.count)
                print('SUCCESS:', response.url)

        yield from response.follow_all(css='a[href^="/"]::attr(href)',
                                       callback=self.parse)
