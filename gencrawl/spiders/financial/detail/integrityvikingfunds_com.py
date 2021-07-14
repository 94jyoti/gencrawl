from gencrawl.spiders.financial.financial_detail_spider import FinancialDetailSpider
from gencrawl.spiders.financial.financial_detail_field_mapping import FinancialDetailFieldMapSpider
from gencrawl.items.financial.financial_detail_item import FinancialDetailItem
import scrapy


class IntegrityvikingfundsComDetail(FinancialDetailSpider):
    name = 'financial_detail_integrityvikingfunds_com'

    def get_items_or_req(self, response, default_item=None):
        default_item = default_item or dict()
        parsed_items = []
        for item in self.prepare_items(response, default_item):
            managers = item.get("temp_fund_managers")
            if managers:
                managers = managers[0].split(";")
                managers = [m.split(",")[0].strip() for m in managers]
                item['fund_managers'] = [{"fund_manager": i} for i in managers]
            parsed_items.append(self.generate_item(item, FinancialDetailItem))
        return parsed_items
