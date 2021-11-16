from gencrawl.pipelines import BaseCustomPipeline
from gencrawl.util.utility import Utility


class CustomPipeline(BaseCustomPipeline):

    def process_item(self, item, spider):
        return super().process_item(item, spider)
