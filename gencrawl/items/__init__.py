# -*- coding: utf-8 -*-

# The main item, every item class should inherit this item class
# unless it has totally different scope

from scrapy import Field, Item


class BaseItem(Item):
    website = Field()
    language = Field()
    country = Field()
    input_url = Field()
    crawl_datetime = Field()
    http_status = Field()
    job_id = Field()
    temp_fields = Field()




