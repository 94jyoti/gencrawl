from gencrawl.util.utility import Utility
import logging
logger = logging.getLogger(__name__)


class BaseCustomPipeline:
    def process_item(self, item, spider):
        custom_method_name = Utility.get_config_name(spider.config['website'])
        try:
            custom_method = getattr(self, custom_method_name)
            logging.info(f"Custom pipeline logic is being called - {custom_method_name}")
            item = custom_method(item, spider)
        except AttributeError:
            pass
        return item
