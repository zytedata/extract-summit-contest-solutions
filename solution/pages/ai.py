from typing import Annotated

import attrs
from scrapy_zyte_api import ExtractFrom
from web_poet import field, handle_urls, HttpResponse
from zyte_common_items import AutoProductPage, Product


@handle_urls("zzcvcpnfzoogpxiqupsergvrmdopqgrk-744852047878.us-south1.run.app")
@attrs.define
class AIContestProductPage(AutoProductPage):
    product: Annotated[Product, ExtractFrom.httpResponseBody]
    response: HttpResponse

    @field
    async def aggregateRating(self):
        value = self.product.aggregateRating
        if value.ratingValue is None:
            css = "[data-rtl-id='reviewsHeaderReviewsAverage']::text"
            value.ratingValue = float(self.response.css(css).get())
        return value

    @field
    async def name(self):
        xpath = '//link[@rel="canonical"][contains(@href, "https://www.homedepot.com/p/")]'
        if self.response.xpath(xpath):
            return self.response.css("h1::text").get().strip()
        return self.product.name

    @field
    async def price(self):
        if value := self.response.css('[data-name-id="PriceDisplay"]'):
            return value
        return self.product.price

    @field
    async def sku(self):
        xpath = '//link[@rel="canonical"][contains(@href, "https://www.homedepot.com/p/")]'
        if self.response.xpath(xpath):
            xpath = '//h2[contains(text(), "SKU")]//span/text()'
            return self.response.xpath(xpath).get().strip()
        return self.product.sku
