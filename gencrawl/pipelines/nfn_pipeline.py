from gencrawl.items.financial.financial_detail_item import FinancialDetailItem
from gencrawl.util.utility import Utility
from gencrawl.util.statics import Statics
import csv
import os
from gencrawl.settings import RES_DIR


class NFNPipeline:

    def __init__(self):
        field_mapping_file = "nfn_field_mapping.csv"
        field_mapping_file = os.path.join(RES_DIR, field_mapping_file)
        self.field_mapping = dict()
        self.redundant_fields = {"total_net_assets": "total_net_assets_date",
                                 "turnover_rate": "turnover_rate_date", "sector_allocation": "sector_allocation_date",
                                 "country_diversification": "country_diversification_date", "portfolio_assets":
                                 "portfolio_assets_date", "number_of_shareholders": "number_of_shareholders_date",
                                 "total_shares_outstanding": "total_shares_outstanding_date",
                                 "duration": "duration_as_of_date", "average_weighted_maturity": "average_weighted_maturity_as_of_date",
                                 "average_weighted_effective_maturity": "average_weighted_effective_maturity_as_of_date",
                                 "sec_yield": "sec_yield_date", "regional_diversification": "regional_diversification_date",
                                 "effective_duration": "effective_duration_date", "weighted_average_duration":
                                 "weighted_average_duration_as_of_date", "average_effective_duration":
                                 "average_effective_duration_as_of_date", "sec_yield_7_day": "sec_yield_date_7_day",
                                 "effective_yield_7_day": "current_yield_date_7_day", "sec_yield_without_waivers_30_day":
                                 "sec_yield_without_waivers_date_30_day", "sec_yield_30_day": "sec_yield_date_30_day"}
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
                    for index, val in enumerate(value, start=1):
                        parsed_item[f'{self.field_mapping[key]} {index}'] = self.parse_field(val)
            else:
                parsed_item[self.field_mapping[key]] = self.parse_field(value)
        return parsed_item

    def remove_redundant_fields(self, item):
        for k, v in self.redundant_fields.items():
            if not item.get(k):
                item[v] = None
        return item

    def replace_none_with_blank_string(self, item):
        for k in item.keys():
            v = item[k]
            if v is None:
                item[k] = ''
        return item

    def process_item(self, item, spider):
        if isinstance(item, FinancialDetailItem):
            item = self.remove_redundant_fields(item)
            item = self.parse_item(item)
            item = self.replace_none_with_blank_string(item)
        return item
