from gencrawl.items.financial.financial_detail_item import FinancialDetailItem
from gencrawl.util.utility import Utility
from gencrawl.util.statics import Statics
import csv
import os
from gencrawl.settings import RES_DIR


class DHCPipeline:

    def process_item(self, item, spider):
        return item
