from gencrawl.items.financial.financial_detail_item import FinancialDetailItem
from gencrawl.util.utility import Utility
from gencrawl.util.statics import Statics
import csv
import os


class NFNPipeline:

    def __init__(self):
        field_mapping_file = "nfn_field_mapping.csv"
        field_mapping_file = os.path.join(os.getcwd(), Statics.RES_DIR, field_mapping_file)
        self.field_mapping = dict()
        for row in Utility.read_csv(field_mapping_file):
            self.field_mapping[row['key']] = row['value']

    def parse_field(self, field):
        if isinstance(field, bool):
            field = "true" if field else "false"
        elif isinstance(field, int) or isinstance(field, float):
            field = str(field)
        return Utility.sanitize(field)

    def parse_item(self, item):
        parsed_item = dict()
        for key in item.keys():
            if key not in self.field_mapping:
                continue

            value = item[key]
            if isinstance(value, list):
                if value and isinstance(value[0], dict):
                    for index, val in enumerate(value, start=1):
                        for k, v in val.items():
                            parsed_item[f'{self.field_mapping[k]} {index}'] = self.parse_field(v)
                else:
                    for val in enumerate(value, start=1):
                        parsed_item[f'{self.field_mapping[k]} {index}'] = self.parse_field(val)
            else:
                parsed_item[self.field_mapping[key]] = self.parse_field(value)
        return parsed_item

    def process_item(self, item, spider):
        if isinstance(item, FinancialDetailItem):
            item = self.parse_item(item)
        return item
