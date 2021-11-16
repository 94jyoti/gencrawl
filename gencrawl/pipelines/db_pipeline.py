from scrapy.exceptions import NotConfigured
from gencrawl.util.statics import Statics
from gencrawl.dal import DAL

class DBPipeline:

    def __init__(self, settings):
        if settings['ENVIRONMENT'] != Statics.ENV_PROD:
            raise NotConfigured
        self.settings = settings
        self.items = list()

    def open_spider(self, spider):
        self.client = spider.client

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def close_spider(self, spider):
        # dump if any items are pending
        if self.items:
            self.insert_items(self.items)

    def process_item(self, item, spider):
        self.items.append(item)
        # if len of items exceeds the batch size, insert to db and initialize it
        if len(self.items) >= spider.settings.get("DB_BATCH_SIZE"):
            self.insert_items(self.items)
            self.items = list()
        return item

    def insert_items(self, items):
        DAL(self.settings, self.client).insert_raw_output(items)

