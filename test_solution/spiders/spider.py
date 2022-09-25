import json

from scrapy import Spider

from test_solution.items import TestItemLoader


class TestSpider(Spider):
    name = "test_spider"
    start_urls = ["https://web-5umjfyjn4a-ew.a.run.app/clickhere"]

    def parse(self, response):
        item_links = response.css(".gtco-practice-area-item .gtco-copy a")
        yield from response.follow_all(item_links, self.parse_item)

        page_links = response.xpath("//a[contains(text(), 'Next Page')]")
        yield from response.follow_all(page_links)

    def parse_item(self, response):
        recommended_links = response.css(".team-item a")
        yield from response.follow_all(recommended_links, self.parse_item)

        il = TestItemLoader(response=response)
        il.add_css("item_id", "#uuid::text")
        il.add_css("name", "h2.heading-colored::text")

        image_id_css = ".img-shadow ::attr(src)"
        image_id_pattern = r"/([\da-f-]+)\.jpg"
        image_id = response.css(image_id_css).re_first(image_id_pattern)
        if not image_id:
            script_xpath = "//script[contains(text(), 'mainimage')]"
            image_id = response.xpath(script_xpath).re_first(image_id_pattern)
        if image_id:
            il.add_value("image_id", image_id)

        rating = response.css('p:contains("Rating") span::text').get()
        if "NO RATING" in rating:
            yield from response.follow_all(
                response.css("::attr(data-price-url)"),
                callback=self.parse_rating,
                cb_kwargs={"item": il.load_item()},
            )
            return
        il.add_value("rating", rating)

        yield il.load_item()

    def parse_rating(self, response, item):
        data = json.loads(response.text)
        il = TestItemLoader(item=item)
        il.add_value("rating", data.get("value"))
        yield il.load_item()
