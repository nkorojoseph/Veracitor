from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.loader import ItemLoader, XPathItemLoader
from scrapy.contrib.loader.processor import TakeFirst
from scrapy import log
from urlparse import urlparse

from ..xpaths import Xpaths
from ..items import ArticleItem, ArticleLoader, ProducerItem
from .articleSpider import ArticleSpider



class NewspaperBankSpider(CrawlSpider):
    name = "newspaperBank"

    def __init__(self, *args, **kwargs):
        
        domain = "http://www.listofnewspapers.com"

        self.start_urls = ["http://www.listofnewspapers.com/en/europe/newspapers-in-west-midlands.html"]
        self.rules = (
            Rule(
                SgmlLinkExtractor(restrict_xpaths = "//li[@class='linewspapers']", deny_domains=domain),
                callback = "parse_webpage_link"
            ),
            Rule(
                SgmlLinkExtractor(restrict_xpaths = "//li[@class='linewspapers']", allow_domains=domain)
            ),
        )
        log.msg("initiated")
        super(NewspaperBankSpider, self).__init__(*args, **kwargs)
        
    def parse_webpage_link(self, response):
        log.msg("found link")
        return ProducerItem(url = response.url)