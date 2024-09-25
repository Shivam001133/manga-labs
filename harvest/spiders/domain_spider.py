# domain_scraper/spiders/domain_spider.py
import scrapy
from helpers.model_helpers import get_domain_info


class DomainSpider(scrapy.Spider):
    name = "domain_spider"

    def __init__(self, domain_name=None, *args, **kwargs):
        domain_name = domain_name.strip()
        harvest = get_domain_info(domain_name)
        self.domain_name = list(harvest.domain_name)
        self.start_urls = list(harvest.domain_url)

    def parse(self, response):
        pass
