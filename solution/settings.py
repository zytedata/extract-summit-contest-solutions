from itemadapter import ItemAdapter
from zyte_common_items import ZyteItemAdapter

ItemAdapter.ADAPTER_CLASSES.appendleft(ZyteItemAdapter)

BOT_NAME = "solution"
SPIDER_MODULES = [
    "zyte_spider_templates.spiders",
]

ADDONS = {
    "solution.addons.SolutionAddon": 250,
    "scrapy_zyte_api.Addon": 500,
}

ITEM_PIPELINES = {
    "solution.item_pipelines.SolutionItemPipeline": 0,
}

SCRAPY_POET_DISCOVER = [
    "solution.pages.common",
]
