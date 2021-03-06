# -*- coding: utf-8 -*-
import scrapy
from AmazonCrapy.mysqlpipelines.sql import Sql
from AmazonCrapy.items import CateItem

class CateSpider(scrapy.Spider):
    name = 'cate'
    custom_settings = {
        'LOG_LEVEL': 'ERROR',
        'LOG_ENABLED': True,
        'LOG_STDOUT': True
    }
    level = 1

    def start_requests(self):
        urls = [
            'https://www.amazon.com/Best-Sellers/zgbs/',
        ]
        Sql.clear_cate(self.level)
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, meta={'level': self.level})
    def parse(self, response):
        # print("获取到的内容为")
        # print(response.body)
        filename = "test.html"
        with open(filename,"wb")as f:
            f.write(response.body)
        print(response.meta['level'])
        if response.meta['level'] == 1:
            list = response.css('#zg_browseRoot ul')[0].css('li a')
        elif response.meta['level'] == 2:
            list = response.css('#zg_browseRoot ul')[0].css('ul')[0].css('li a')
        else:
            return 0
        item = CateItem()
        leve_cur = response.meta['level']
        response.meta['level'] = response.meta['level'] + 1

        for one in list:
            item['title'] = one.css('::text')[0].extract()
            link = one.css('::attr(href)')[0].extract()
            item['link'] = link.split('ref=')[0]
            item['level'] = leve_cur
            item['pid'] = 1
            yield item
            if int(float(self.level)) > 1:
                print("展开二级访问URl:"+item['link'])
                yield scrapy.Request(url=item['link'], callback=self.parse, meta=response.meta)