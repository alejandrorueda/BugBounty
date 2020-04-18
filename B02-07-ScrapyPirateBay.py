#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Adastra

from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy import Request
from scrapy.item import Item, Field
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.xlib.pydispatch import dispatcher
from twisted.internet import reactor
from scrapy import signals
from scrapy.utils.project import get_project_settings
from scrapy.crawler import Crawler

class Torrent(Item):
    url = Field()
    tipo = Field()
    torrentLink = Field()
    size = Field()
    description = Field()

class PirateBaySpider(CrawlSpider):

    name = 'thepiratebay.se'
    allowed_domains = ['thepiratebay.se']
    start_urls = ['http://thepiratebay.se/browse']
    rules = [Rule(LinkExtractor(allow=['/\d+']), 'parse_torrent')]

    def parse_torrent(self, response):
        print "Torrent"
        x = Selector(response)
        torrent = Torrent()
        torrent['url'] = response.url
        torrent['tipo'] = x.select('//*[@id="searchResult"]/tr[1]/td[1]/center/a[2]//text()').extract()
        torrent['torrentLink'] = x.select('//*[@id="searchResult"]/tr[1]/td[2]/a[2]/@href').extract()
        torrent['description'] = x.select('//*[@id="searchResult"]/tr[1]/td[2]/div/a/@title').extract()
        torrent['size'] = x.select('//*[@id="searchResult"]/tr[1]/td[2]/font/text()[2]').extract()
        return torrent


def catch_item(sender, item, **kwargs):
    print "[+] Processing Item %s ...  " %(item)

if __name__ == '__main__':
    dispatcher.connect(catch_item, signal=signals.item_passed)
    dispatcher.connect(reactor.stop, signal=signals.spider_closed)

    settings = get_project_settings()
    crawler = Crawler(settings)
    crawler.configure()
    
    spider = PirateBaySpider()
    crawler.crawl(spider)
    print "\n[+] Starting scrapy engine..."
    crawler.start()
    reactor.run()