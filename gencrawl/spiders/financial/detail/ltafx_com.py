from gencrawl.spiders.financial.financial_detail_spider import FinancialDetailSpider
from gencrawl.spiders.financial.financial_detail_field_mapping import FinancialDetailFieldMapSpider

class ItafxComDetail(FinancialDetailFieldMapSpider):
    name = 'financial_detail_itafx_com'
    def get_items_or_req(self, response, default_item=None):
        parsed_items = super().get_items_or_req(response, default_item)
        leng = len(parsed_items)
        return parsed_items