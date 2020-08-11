import json

import scrapy
from datetime import datetime

OUTPUT = 'J:/PycharmProject/Crawler_News/tutorial/tutorial/spiders/output/TinTuc/tintuc_{}.txt'.format(
    datetime.now().strftime('%Y%m%d_%H%M%S'))


class TinTuc_Crawler(scrapy.Spider):
    name = 'tintuc_crawler'
    allowed_domains = ['tintuc.vn']
    start_urls = ['https://tintuc.vn']
    count = 0

    def parse(self, response):
        if response.status == 200 and response.css(
                'meta[property="og:url"]::attr("content")').get() != "https://tintuc.vn":
            print('Crawling from: ' + response.url)
            data = {
                'Link': response.url,
                'Title': response.css('h1.article-title::text').get(),
                'Content': '\n'.join([
                    ''.join(crawl.css('*::text').getall())
                    for crawl in response.css('div.content_article p')
                ]),
                'Date': response.css('ul.nav > li[class="publish-date dim w125"] > a::text').get(),
                #                'Tags': response.css('meta[name="its_tag"]::attr("content")').get()
            }
            with open(OUTPUT, 'a', encoding='utf8') as fi:
                fi.write(json.dumps(data, ensure_ascii=False))
                fi.write('\n')
                self.count += 1
                self.crawler.stats.set_value('Count', self.count)
                print(self.count)
                print('SUCCESS:', response.url)

        yield from response.follow_all(css='a[href^="https://tintuc.vn"]::attr(href), a[href^="/"]::attr(href)',
                                       callback=self.parse)
