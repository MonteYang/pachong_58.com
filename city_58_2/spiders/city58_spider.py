# -*- coding: utf-8 -*-
from traceback import format_exc

import scrapy
from scrapy.http import Request
from ..utils.parse import get_xiaoqu_detail_url
from ..utils.parse import parse_xiaoqu_detail
from ..utils.parse import get_ershou_price_list

from ..items import City58XiaoQu


class City58SpiderSpider(scrapy.Spider):
    name = 'city58_spider'
    allowed_domains = ['58.com']
    # start_urls = ['http://58.com/']
    host = 'bj.58.com'
    xiaoqu_url_format = 'http://{}/xiaoqu/{}/'
    xiaoqu_code = list()
    xiaoqu_code.append(1142)

    def start_requests(self):
        start_urls = [self.xiaoqu_url_format.format(self.host, code) for code in self.xiaoqu_code]
        self.logger.debug(start_urls)
        for url in start_urls:
            yield Request(url)

    def parse(self, response):
        '''
        :param response:
        :return:
        '''
        xiaoqu_url_list = get_xiaoqu_detail_url(response)
        for url in xiaoqu_url_list:
            yield Request(url,
                          callback=self.xiaoqu_detail,
                          errback=self.error_back
                          )

    def xiaoqu_detail(self, response):
        data = parse_xiaoqu_detail(response)
        item = City58XiaoQu()
        item.update(data)  # !!!!!!!!!!!
        item['id'] = response.url.split('/')[4]
        yield item

        # 二手房
        url = 'http://{}/xiaoqu/{}/ershoufang/'.format(self.host, item['id'])
        yield Request(url,
                      callback=self.ershoufang_price_list,
                      errback=self.error_back,
                      meta={'id': item['id']}
        )

        # 出租房
        chuzu_url = 'http://{}/xiaoqu/{}/chuzu/'.format(self.host, item['id'])
        yield Request(url,
                      callback=self.chuzufang_url_list,
                      errback=self.error_back,
                      meta={'id': item['id']}
        )

    def ershoufang_price_list(self, response):
        price_list = get_ershou_price_list(response)
        yield {'id':response.meta['id'], 'price_list': price_list}

        # 翻页

    def chuzufang_url_list(self, response):
        pass

    def error_back(self, e):
        _ = e# 占位
        self.logger.error(format_exc())