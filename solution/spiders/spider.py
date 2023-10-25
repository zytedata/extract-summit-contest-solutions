import json
import re

from number_parser import parse_number
from scrapy import Request, Spider

from ..items import SolutionItemLoader


class SolutionSpider(Spider):
    name = "solution"

    custom_settings = {
        "USER_AGENT": "GoodRobot",
    }

    def start_requests(self):
        yield Request(
            "https://ducqocgbcrqftlrn-5umjfyjn4a-ew.a.run.app/items",
            callback=self.parse_item_list,
        )
        yield Request(
            "https://ducqocgbcrqftlrn-5umjfyjn4a-ew.a.run.app/sitemap.xml",
            callback=self.parse_sitemap,
        )

    def parse_item_list(self, response):
        item_links = response.xpath("//a[.//h3]")
        yield from response.follow_all(item_links, self.parse_item)

        page_links = response.xpath("//a[contains(text(), '→')]")
        yield from response.follow_all(page_links, self.parse_item_list)

    def parse_sitemap(self, response):
        selector = response.selector
        selector.remove_namespaces()
        for loc in selector.xpath("//loc/text()"):
            yield response.follow(loc, callback=self.parse_item)

    def parse_item(self, response):
        il = SolutionItemLoader(response=response)
        il.add_css("item_id", "#uuid::text")
        il.add_css("text", 'pre::text')

        stock_words = response.css(".stock::text").get()
        stock = parse_number(stock_words)
        il.add_value("stock", stock)

        yield il.load_item()
