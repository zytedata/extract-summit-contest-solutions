from dataclasses import dataclass, field
from typing import Optional

from itemloaders.processors import Compose, Join, TakeFirst
from scrapy.loader import ItemLoader


@dataclass
class TestItem:
    item_id: str = field(default_factory=str)
    name: str = field(default_factory=str)
    image_id: Optional[str] = field(default=None)
    rating: str = field(default_factory=str)


class TestItemLoader(ItemLoader):
    default_item_class = TestItem
    default_output_processor = Compose(Join(), str.strip)
    image_id_out = TakeFirst()
