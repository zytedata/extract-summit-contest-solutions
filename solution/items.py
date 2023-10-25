from dataclasses import dataclass, field
from typing import Optional

from itemloaders.processors import Compose, Join
from scrapy.loader import ItemLoader


class TakeLast:
    def __call__(self, values):
        return values[-1]


@dataclass
class SolutionItem:
    item_id: str = field(default_factory=str)
    text: str = field(default_factory=str)
    stock: int = field(default_factory=int)


class SolutionItemLoader(ItemLoader):
    default_item_class = SolutionItem
    default_output_processor = Compose(Join(), str.strip)
    stock_out = Compose(TakeLast(), int)
