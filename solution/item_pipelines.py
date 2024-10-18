from .items import SolutionItem


class SolutionItemPipeline:
    def process_item(self, item, spider):
        return SolutionItem(
            url=item.url,
            name=item.name,
            brand=item.brand.name,
            sku=item.sku,
            price=item.price,
            rating=item.aggregateRating.ratingValue,
            reviews=item.aggregateRating.reviewCount,
        )
