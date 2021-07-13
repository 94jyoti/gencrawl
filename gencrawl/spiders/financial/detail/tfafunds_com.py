from gencrawl.spiders.financial.financial_detail_spider import FinancialDetailSpider
from gencrawl.spiders.financial.financial_detail_field_mapping import FinancialDetailFieldMapSpider
from gencrawl.items.financial.financial_detail_item import FinancialDetailItem
import scrapy
from gencrawl.util.statics import Statics


class TfafundsComDetail(FinancialDetailFieldMapSpider):
    name = 'financial_detail_tfafunds_com'

    def prepare_mapped_items(self, response, items):
        parsed_items = []
        classes = response.xpath("//h3[contains(text(), 'Class ')]/text()").extract_first().split("|")
        for class_block in classes:
            cls, ticker = class_block.split(":")
            if ticker.strip() == 'N/A':
                class_to_remove = cls.strip()
                items = [i for i in items if class_to_remove not in i['share_class']]

        ext_codes = {k: v for k, v in self.ext_codes.items() if v.get("return_type") == Statics.RETURN_TYPE_LIST_MAP}
        fields_to_map = ext_codes.keys()
        for index, item in enumerate(items):
            parsed_items.append(self.map_fields(index, len(items), item, fields_to_map))
        return parsed_items
