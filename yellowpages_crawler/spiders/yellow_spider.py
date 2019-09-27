# -*- coding: utf-8 -*-
import scrapy
from scrapy.crawler import CrawlerProcess

class YellowSpiderSpider(scrapy.Spider):
    name = 'yellow_spider'
    page_number = 2
    api='http://api.scraperapi.com/?api_key=822da7f5e247570657b28227f6d782f1&url='#a string containing http request to scraperapi.com to bypass restrictions like IP banning and Bot detection
    link ='https://www.yellowpages.com/los-angeles-ca/restaurants'
    start_urls = [api+link]

    def parse(self, response):
        holders = response.css('div.info')

        for holder in holders:
            yield{name: holder.css('h2.n').css('a').css('span::text').extract_first(),

            website:holder.css('a.track-visit-website::attr(href)').extract_first(),

            phone: holder.css('div.phones.phone.primary::text').extract_first(),

            address:holder.css('div.street-address::text').extract_first(),

            locality:holder.css('div.locality::text').extract_first()}

        next_page = YellowSpiderSpider.api+'https://www.yellowpages.com/los-angeles-ca/restaurants?page='+str(YellowSpiderSpider.page_number)
        if YellowSpiderSpider.page_number<35:
            YellowSpiderSpider.page_number+=1
            yield scrapy.Request(url=next_page, callback = self.parse)

process = CrawlerProcess(settings={
    'FEED_FORMAT': 'csv',
    'FEED_URI': 'YellowPages-output'
})

process.crawl(YellowSpiderSpider)
process.start() # the script will block here until the crawling is finished
