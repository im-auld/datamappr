from scrapy.spider import Spider
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from govdata.items import GovdataItem
from scrapy.http import Request

class govdata_spider(Spider):
    name = 'stlouisfed'
    allowed_domains = ["research.stlouisfed.org"]
    start_urls = ["http://research.stlouisfed.org/fred2/categories/27281"]
   
    
    def parse(self, response):
        sel = Selector(response)
        datalinks = sel.xpath('//td[@valign]/ul[@class="list-bullets"]/li/a')
        for datalink in datalinks:
            states = datalink.xpath('text()').extract()
            hrefs = datalink.xpath('@href').extract()
            for state, href in zip(states, hrefs):
                yield Request(url=''.join(('http://research.stlouisfed.org',
                                href, '/downloaddata')),
                             callback=self.parse_item,
                             meta={'state':state})

    def parse_item(self, response):
        sel = Selector(response)
        item = GovdataItem()
        item['state'] = response.meta['state']
        item['link'] = sel.xpath('//a/@href[contains(.,"_csv_")]').extract() 
        return item
                        