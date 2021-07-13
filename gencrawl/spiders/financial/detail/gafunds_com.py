from gencrawl.spiders.financial.financial_detail_spider import FinancialDetailSpider
from gencrawl.spiders.financial.financial_detail_field_mapping import FinancialDetailFieldMapSpider
import scrapy
from gencrawl.util.statics import Statics


class GafundsComDetail(FinancialDetailFieldMapSpider):
    name = 'financial_detail_gafunds_com'

    def get_header_index(self, response, value):
        headers = response.xpath("//table[@id='fund_details_table']//tr[1]/td/text()").extract()
        return headers.index(value) + 1

    def map_fields(self, index, total_len, item, fields_to_map, response=None):
        item = super(GafundsComDetail, self).map_fields(index, total_len, item, fields_to_map)
        # custom logic of adding total_expense_gross and total_expense_net
        if total_len > 1:
            i = self.get_header_index(response, item['nasdaq_ticker'])
            value = response.xpath(
                f"//td[contains(text(), 'Expense Ratio')]/parent::tr/td[{i}]//text()").extract()
            for v in value:
                if ' (' not in v:
                    expense_gross = v
                    expense_net = None
                else:
                    if 'net' in v:
                        expense_net = v.split("(")[0]
                    elif 'gross' in v:
                        expense_gross = v.split("(")[0]
            item['total_expense_gross'] = expense_gross
            item['total_expense_net'] = expense_net
        return item
