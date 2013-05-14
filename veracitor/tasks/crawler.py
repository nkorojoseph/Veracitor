# crawler.py
# ===========
# Defines tasks for the crawler.

try:
    from veracitor.tasks.tasks import taskmgr
except:    
    from tasks import taskmgr
    
from ..crawler import crawlInterface as ci

from veracitor.database import *

@taskmgr.task
def scrape_article(url):
    ci.scrape_article(url)
    return { "producer": extractor.entity_to_dict(extractor.get_producer_with_url(url)) }



@taskmgr.task
def add_newspaper(url):
    ci.add_newspaper(url)
    return { "producer": extractor.entity_to_dict(extractor.get_producer_with_url(url)) }
    

    
@taskmgr.task
def request_scrape(url):
    ci.request_scrape(url)
    return { "producer": extractor.entity_to_dict(extractor.get_producer_with_url(url)) }
