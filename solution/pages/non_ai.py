import re

import attrs
from web_poet import field, handle_urls
from zyte_common_items import AggregateRating, Brand, ProductPage


@handle_urls("zzcvcpnfzoogpxiqupsergvrmdopqgrk-744852047878.us-south1.run.app")
@attrs.define
class NonAIContestProductPage(ProductPage):

    @field
    async def aggregateRating(self):
        rating_css = """
        .reviewCountTextLinkedHistogram .a-size-base::text,
        .ux-summary__start--rating span::text,
        .ugc-c-review-average::text,
        [data-rtl-id='reviewsHeaderReviewsAverage']::text
        """
        rating = self.response.css(rating_css).get()
        if rating:
            rating = float(rating)

        reviews_css = """
        #acrCustomerReviewText::text,
        .ux-summary__count span::text,
        .c-reviews::text,
        [data-rtl-id='reviewsHeaderReviewsLink']::text
        """
        reviews = self.response.css(reviews_css).get()
        if reviews:
            reviews = int(reviews.split(" ")[0].replace(",", "").replace("(", ""))

        return AggregateRating(ratingValue=rating, reviewCount=reviews)

    @field
    async def brand(self):
        css = """
        .po-brand .po-break-word::text,
        .ux-labels-values--brand dd span::text,
        .shop-product-title a::text,
        .product-details h2::text,
        [data-rtl-id="listingManufacturerName"] a::text
        """
        name = self.response.css(css).get()
        return Brand(name=name)

    @field
    async def name(self):
        css = """
        #productTitle::text,
        .x-item-title__mainTitle ::text,
        [itemprop="name"] ::text
        """
        name = self.response.css(css).get()
        if not name:
            name = self.response.css("h1 ::text").get()
        if name:
            name = name.strip()
        return name

    @field
    async def price(self):
        css = """
        #twister-plus-price-data-price::attr(value),
        .x-price-primary,
        .priceView-hero-price,
        [data-name-id="PriceDisplay"]
        """
        value = self.response.css(css)
        if not value:
            value = re.search(r'"price":(\d+\.\d+)', self.response.text)[1]
        return value

    @field
    async def sku(self):
        css = """
        #ASIN::attr(value),
        .ux-layout-section__textual-display--itemId .ux-textspans--BOLD::text,
        .sku .product-data-value::text,
        [name="sku"]::attr(value)
        """
        sku = self.response.css(css).get()
        if not sku:
            xpath = """
            //h2[contains(text(), "SKU")]//span/text()
            """
            sku = self.response.xpath(xpath).get()
        return sku.strip()
