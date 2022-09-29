import json
import re

from scrapy import Request, Spider

from .items import TestItemLoader


class TestSpider(Spider):
    name = "test_spider"

    def start_requests(self):
        yield Request(
            "https://extract-summit-kokb7ng7-5umjfyjn4a-ew.a.run.app/"
        )

    def parse(self, response):
        yield response.follow("/clickhere?sort_by=alphabetically", self.parse_item_list)

    def parse_item_list(self, response):
        item_links = response.css(".gtco-practice-area-item .gtco-copy a")
        yield from response.follow_all(item_links, self.parse_item)

        page_links = response.xpath("//a[contains(text(), 'Next Page')]")
        yield from response.follow_all(page_links, self.parse_item_list)

    def parse_item(self, response):
        recommended_links = response.css(".team-item a")
        yield from response.follow_all(recommended_links, self.parse_item)

        image_id_pattern = r"/([\da-f-]+)\.jpg"
        il = TestItemLoader(response=response)

        phone_pattern = r'cyphered_phone\s*=\s*Array\.from\("([^"]+)'
        encrypted_phone = re.search(phone_pattern, response.text)[1]
        phone = "".join(
            chr(ord(character)-16) for character in encrypted_phone
        )
        il.add_value("phone", phone)

        json_data = response.css('#item-data-json::text').get()
        if json_data:
            data = json.loads(json_data)

            for field in ("item_id", "name"):
                il.add_value(field, data[field])

            if "image_path" in data:
                image_id = re.search(image_id_pattern, data["image_path"])[1]
            else:
                script_xpath = "//script[contains(text(), 'mainimage')]"
                image_id = response.xpath(script_xpath).re_first(image_id_pattern)
            il.add_value("image_id", image_id)

            if "rating" in data:
                il.add_value("rating", data["rating"])
                yield il.load_item()
            else:
                yield response.follow(
                    data["data_url"],
                    callback=self.parse_rating,
                    cb_kwargs={"item": il.load_item()},
                )

            return

        il.add_css("item_id", "#uuid::text")
        il.add_css("name", "h2.heading-colored::text")

        image_id_css = ".img-shadow ::attr(src)"
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
