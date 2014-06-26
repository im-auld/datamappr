from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from govdata.items import GovdataItem

class govdata_spider(CrawlSpider):
    name = 'NO MORE'
    allowed_domains = ["research.stlouisfed.org"]
    start_urls = ["http://research.stlouisfed.org/fred2/categories/27281"]
   
    
    def parse(self, response):
        sel = Selector(response)
        items = []
        datalinks = sel.xpath('//td[@valign]/ul[@class="list-bullets"]/li/a')
        for datalink in datalinks:
            item = GovdataItem()
            item['state'] = datalink.xpath('text()').extract()
            item['link'] = datalink.xpath('@href').extract()
            items.append(item)
        return items