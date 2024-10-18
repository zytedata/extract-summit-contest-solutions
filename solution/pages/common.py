import attrs
from web_poet import field, handle_urls
from zyte_common_items import ProbabilityRequest, ProductNavigationPage


@handle_urls("zzcvcpnfzoogpxiqupsergvrmdopqgrk-744852047878.us-south1.run.app")
@attrs.define
class ContestProductNavigationPage(ProductNavigationPage):

    @field
    async def items(self):
        return [
            ProbabilityRequest(url=self.response.urljoin(href))
            for href in self.response.css("a::attr(href)").getall()
        ]
