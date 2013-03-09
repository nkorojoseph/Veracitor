from scrapy.item import Item, Field
from scrapy.contrib.loader import ItemLoader, XPathItemLoader
from scrapy.contrib.loader.processor import TakeFirst, Compose, Join

class ArticleItem(Item):
    title = Field()
    author = Field()
    date = Field()
    url = Field()
    summary = Field()
    
    def __str__(self):
        return unicode(self).encode('utf-8')
    
    def __unicode__(self):           
        return (self["title"] + " (" + self["author"] + ", " + self["date"] + ")\nURL: " + self["url"] + "\nSUMMARY: " + self["summary"])

    def long_string(self):
        return ("---------------------------------\n"+
                self.__unicode__() +
                "\n---------------------------------"
               );

    def short_string(self):
        return self["title"]


class ArticleLoader(XPathItemLoader):
    default_output_processor = TakeFirst()
    date_out = Join()
    summary_out = Join()
    title_out = Join()
