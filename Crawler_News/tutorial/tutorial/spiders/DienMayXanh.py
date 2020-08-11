import json

import scrapy
from datetime import datetime

OUTPUT = 'J:/PycharmProject/Crawler_News/tutorial/tutorial/spiders/output/dienmayxanh/dmx_{}.txt'.format(datetime.now().strftime('%Y%m%d_%H%M%S'))

class Vnexpress_Crawler(scrapy.Spider):
    name = 'dmx'
    allowed_domains = ['dienmayxanh.com']
    start_urls = ['https://www.dienmayxanh.com']
    count = 0

    def parse(self, response):
        if response.status == 200 and response.css('meta[property="og:url"]::attr("content")').get() != "https://dienmayxanh.com":
            print('Crawling from: ' + response.url)
            data = {
                'link': response.url,
                'title': response.css('section[class="themNoel"] h1::text').get(),
                'Featured Features': '\n'.join([
                    ''.join(c.css('*::text').getall())
                    for c in response.css('div.key-selling ul li')
                ]),

                'Technical Specifications': '\n'.join([
                    ''.join(c.css('*::text').getall())
                    for c in response.css('div.thong-so-ki-thuat ul.specs li')
                ]),
            }
            with open(OUTPUT, 'a', encoding='utf8') as f:
                f.write(json.dumps(data, ensure_ascii=False))
                f.write('\n')
                self.count += 1
                self.crawler.stats.set_value('Count', self.count)
                print(self.count)
                print('SUCCESS:', response.url)

        yield from response.follow_all(css='a[href^="https://www.dienmayxanh.com"]::attr(href), a[href^="/"]::attr(href)',
                                       callback=self.parse)









