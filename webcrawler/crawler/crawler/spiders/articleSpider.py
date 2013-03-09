from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from crawler.xpaths import Xpaths
<<<<<<< HEAD
from crawler.items import ArticleItem
<<<<<<< HEAD
from urlparse import urlparse

=======
=======
from crawler.items import ArticleItem, ArticleLoader
>>>>>>> Fixed spider-loader bug?
from scrapy.contrib.loader import ItemLoader, XPathItemLoader
from scrapy.contrib.loader.processor import TakeFirst
from items import ArticleItem
>>>>>>> itemloaders in spider


class ArticleSpider(BaseSpider):
    name = "article"

    def __init__(self, *args, **kwargs):
        super(ArticleSpider, self).__init__(*args, **kwargs)
        self.start_urls = kwargs.get('start_urls').split(',')

    def parse(self, response):
       return ArticleSpider.scrape_article(response)
        
    @staticmethod
    def scrape_article(response):
        xpaths = Xpaths('crawler/webpages.xml')
        domain = urlparse(response.url)[1]
        loader = ArticleLoader(item=ArticleItem(), response=response)
        
<<<<<<< HEAD
        for xpath in xpaths.get_title_xpaths(domain):
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
            article["title"] = hxs.select(xpath).extract()
            break
        
        for xpath in xpaths.get_author_xpaths(domain):
            article["author"] = hxs.select(xpath).extract()
            break
            
        for xpath in xpaths.get_date_xpaths(domain):
            article["date"] = hxs.select(xpath).extract()
            break
            
        for xpath in xpaths.get_summary_xpaths(domain):
            article["summary"] = hxs.select(xpath).extract()
            break
=======
=======
>>>>>>> Fixed spider-loader bug?
=======
            xpath += "/normalize-space()"
>>>>>>> clean text
            loader.add_xpath("name", xpath)
=======
            loader.add_xpath("title", xpath)
>>>>>>> fixed bugs, added output testing
=======
            loader.add_xpath("title", xpath)
>>>>>>> not sure
        
        for xpath in xpaths.get_author_xpaths(domain):
            loader.add_xpath("author", xpath)
            
        for xpath in xpaths.get_date_xpaths(domain):
            loader.add_xpath("date", xpath)
<<<<<<< HEAD
            
        for xpath in xpaths.get_summary_xpaths(domain):
            loader.add_xpath("summary", xpath)
>>>>>>> itemloaders in spider
=======
           
        for xpath in xpaths.get_summary_xpaths(domain):
            loader.add_xpath("summary", xpath)
<<<<<<< HEAD
>>>>>>> Fixed spider-loader bug?
=======

<<<<<<< HEAD
<<<<<<< HEAD
        open("output", 'wb').write(loader.get_output_value('title'))
>>>>>>> fixed bugs, added output testing
=======
        open("output", "wb").write(loader.get_output_value("title").encode('utf8'))
>>>>>>> stuff n stufff....
            
=======
>>>>>>> removed file write
=======
        for field in ArticleItem.fields.iterkeys():
            for xpath in xpaths.get_xpaths(field, domain):
                loader.add_xpath(field, xpath)
        loader.add_value("url", response.url)
                
>>>>>>> Big commit. Added new spider that crawls entire newspaper from base-url and extracts all valid articles. article-qualification in XML-file is used to filter articles from other links.
        return loader.load_item()
