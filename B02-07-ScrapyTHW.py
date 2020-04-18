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

class HackerWayItem(Item):
	title = Field()
	author =  Field()
	tag = Field()
	date = Field()


class BloggerSpider(CrawlSpider):
	name="TheHackerWay"
	start_urls=['http://thehackerway.com']
	# urls desde las cuales el spider comenzará el proceso de crawling
    	rules = [Rule(LinkExtractor(allow=[r'/\d{4}']), follow=True, callback='parse_blog'), 
    		# r'/\d+' : expression regular para http://thehackerway.com/X URLs
	    	Rule(LinkExtractor(allow=[r'\d{4}/\d{2}/\d{2}/\w+']), callback='parse_blog')]
    		# http://thehackerway.com/YYYY/MM/DD/titulo URLs

	def parse_blog(self, response):
		print 'link parseado %s' %response.url
		hxs = Selector(response)
		item = HackerWayItem()
		item['title'] = hxs.select('//title/text()').extract() # Selector XPath para el titulo
		item['author'] = hxs.select("//span[@class='author']/a/text()").extract() # Selector XPath para el author
		item['tag'] = hxs.select("//meta[@property='og:title']/text()").extract() # Selector XPath para el tag
		item['date'] = hxs.select("//span[@class='date']/text()").extract() # Selector XPath para la fecha
		return item # Retornando el Item.

def catch_item(sender, item, **kwargs):
	print "Item Extraido:", item


if __name__ == '__main__':
    dispatcher.connect(catch_item, signal=signals.item_passed)
    dispatcher.connect(reactor.stop, signal=signals.spider_closed)

    settings = get_project_settings()
    crawler = Crawler(settings)
    crawler.configure()
    
    spider = BloggerSpider()
    crawler.crawl(spider)
    print "\n[+] Starting scrapy engine..."
    crawler.start()
    reactor.run()