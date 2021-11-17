from scrapy.exceptions import NotConfigured
from gencrawl.util.statics import Statics
from gencrawl.dal import DAL
import logging


class DBPipeline:

    def __init__(self, settings):
        self.logger = logging.getLogger(self.__class__.__name__)
        if not settings.get("DB_PIPELINE_ENABLED"):
            raise NotConfigured
        if settings['ENVIRONMENT'] != Statics.ENV_PROD:
            self.logger.info("Environment not PRODUCTION, hence disabling DB Pipeline")
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
        self.logger.info(f"Inserting {len(items)} items to DB")
        DAL(self.settings, self.client).insert_raw_output(items)

