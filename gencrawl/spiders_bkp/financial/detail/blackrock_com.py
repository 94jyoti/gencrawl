from gencrawl.spiders.financial.financial_detail_spider import FinancialDetailSpider
from gencrawl.util.statics import Statics
import json
import scrapy
from gencrawl.items.financial.financial_detail_item import FinancialDetailItem
from datetime import datetime
import datetime
import urllib.parse


class BlackrockComDetail(FinancialDetailSpider):
    name = 'financial_detail_blackrock_com'

    def get_items_or_req(self, response, default_item={}):
        items = self.prepare_items(response, default_item)
        item = items[0]
        api_url = response.xpath(
            "//div[@id='distroTableTab' or @id='distroAllTable']/@data-ajaxuri").extract_first()
        meta = response.meta
        meta['items'] = item
        item['api_url'] = api_url
        r = self.make_request(response.urljoin(api_url), callback=self.parse_performance_response, meta=meta)
        return r

    def parse_performance_response(self, response):
        items = response.meta['items']
        response_json = json.loads(response.text)
        capital_gains_list = []
        dividend_history = []
        for i in response_json.get('all.table', response_json.get('table'))['aaData']:
            data_dict1 = {"ex_date": "", "pay_date": "", "ordinary_income": "", "qualified_income": "",
                          "record_date": "", "per_share": "", "reinvestment_price": ""}
            data_dict2 = {'long_term_per_share': "", 'cg_ex_date': "", 'cg_record_date': "", 'cg_pay_date': "",
                              'short_term_per_share': "", 'total_per_share': "", 'cg_reinvestment_price': ""}
            data_dict1['record_date'] = i[0]['display']
            data_dict1['ex_date'] = i[2]['display']
            data_dict1['per_share'] = i[3]['display']
            data_dict1['pay_date'] = i[1]['display']
            data_dict1['ordinary_income'] = i[4]['display']
            dividend_history.append(data_dict1)
            data_dict2['long_term_per_share'] = i[6]['display']
            data_dict2['cg_ex_date'] = i[2]['display']
            data_dict2['cg_record_date'] = i[0]['display']
            data_dict2['short_term_per_share'] = i[5]['display']
            data_dict2['total_per_share'] = i[3]['display']
            data_dict2['cg_pay_date'] = i[1]['display']
            capital_gains_list.append(data_dict2)

        items['capital_gains'] = capital_gains_list
        items['dividends'] = dividend_history
        yield self.generate_item(items, FinancialDetailItem)
