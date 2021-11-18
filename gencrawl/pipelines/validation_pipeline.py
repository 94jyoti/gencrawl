import hashlib
import logging
from scrapy.exceptions import NotConfigured
from scrapy.exceptions import DropItem


class ValidationPipeline(object):
    """Validation of items basis on some fields.
    """
    def __init__(self, settings):
        self.logger = logging.getLogger(self.__class__.__name__)
        if not settings.getbool('ITEM_VALIDATION_ENABLED'):
            raise NotConfigured

    def open_spider(self, spider):
        self.fields = list(set(spider.settings.getlist("VALIDATION_FIELDS")))
        client_fields = spider.settings.getlist(f'{spider.client}_VALIDATION_FIELDS')
        if client_fields:
            self.fields = set(self.fields + client_fields)
        self.logger.info(f"Any item not having any of these fields will be dropped - {','.join(self.fields)}")

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_item(self, item, spider):
        """Checks whether a scrapy item is having all of the fields"""
        for field in self.fields:
            if not item.get(field):
                raise DropItem(
                    'Field <{}> not found in item <{}>'.format(field, item))
        return item


