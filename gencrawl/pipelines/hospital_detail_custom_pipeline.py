from gencrawl.pipelines import BaseCustomPipeline
from gencrawl.util.utility import Utility


class CustomPipeline(BaseCustomPipeline):

    """
    Sample custom logic method for website cassregional.org
    method name should be website name removing https:// and www
    it should accept item & spider in argument and it should return the item
    """
    def cassregional_org(self, item, spider):
        # custom logic here
        return item

    def process_item(self, item, spider):
        return super().process_item(item, spider)
