from gencrawl.spiders.financial.financial_detail_spider import FinancialDetailSpider
from gencrawl.spiders.financial.financial_detail_field_mapping import FinancialDetailFieldMapSpider
import scrapy
import json


class GrFundsComDetail(FinancialDetailFieldMapSpider):
    name = 'financial_detail_gr_funds_com'
    allowed_domains = ["pqzo2gxpoa.execute-api.us-east-1.amazonaws.com"]

    def get_items_or_req(self, response, default_item=None):
        items = super().get_items_or_req(response, default_item)
        distributions_request = self.make_request(
            "https://pqzo2gxpoa.execute-api.us-east-1.amazonaws.com/production/api/distributions/", self.parse_dist,
            meta={"items": items}, dont_filter=True)
        return [distributions_request]

    def parse_dist(self, response):
        items = response.meta['items']
        jsn_resp = json.loads(response.text)
        data = json.loads(jsn_resp['rows'])

        for item in items:
            capital_gains = []
            dividends = []
            item['capital_gains'] = capital_gains
            item['dividends'] = dividends
            for d in data:
                if d[0] == item['nasdaq_ticker']:
                    cg = {"cg_ex_date": d[3], "cg_record_date": d[2], "cg_pay_date": d[4], "short_term_per_share":
                          d[7], "long_term_per_share": d[6]}
                    capital_gains.append(cg)
                    div = {"ex_date": d[3], "record_date": d[2], "pay_date": d[4], "ordinary_income": d[5]}
                    dividends.append(div)

            yield item

