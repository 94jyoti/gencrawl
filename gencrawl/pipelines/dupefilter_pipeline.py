import hashlib
import logging
from scrapy.exceptions import NotConfigured
from scrapy.exceptions import DropItem


class DupeFilterPipeline(object):
    """De duplication of items basis on some fields.
    """
    def __init__(self, settings):
        self.logger = logging.getLogger(self.__class__.__name__)
        if not settings.getbool('ITEM_DUPEFILTER_ENABLED'):
            raise NotConfigured
        self._itemversion_cache = {}

    def open_spider(self, spider):
        self.client = spider.client
        self.fields = set(spider.settings.getlist(f'{spider.client}_DUPEFILTER_FIELDS'))

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_item(self, item, spider):
        """Checks whether a scrapy item is a dupe, based on version (not vary)
        fields of the item class"""
        version = self.create_item_version(item, self.fields or item.fields)
        item['unique_hash'] = version
        if version in self._itemversion_cache:
            old_url = self._itemversion_cache[version]
            raise DropItem(
                'Duplicate product scraped at <{}>, first one was scraped at '
                '<{}>'.format(item[spider.url_key], old_url))
        self._itemversion_cache[version] = item[spider.url_key]
        return item

    def create_item_version(self, item, fields):
        """Item version based on hashlib.sha1 algorithm"""
        _hash = hashlib.sha1()
        for attrname in fields:
            _hash.update(repr(item.get(attrname) or '').encode('utf-8'))
        return _hash.hexdigest()

