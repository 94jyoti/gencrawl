from gencrawl.spiders.financial.financial_detail_spider import FinancialDetailSpider
from gencrawl.util.statics import Statics
import json


class PgimComDetail(FinancialDetailSpider):
    name = 'financial_detail_pgim_com'
    performance_api = "https://www.pgim.com/pcom6/services/pcom/reportjson?&pageid=1&fundname={fund_name}&fundid=undefined"

    def parse_navigation(self, response, items):
        fund_name = response.request.url.split("/")[-1]
        performance_api = self.performance_api.format(fund_name=fund_name)
        meta = response.meta
        meta['items'] = items
        return self.make_request(performance_api, callback=self.parse_performance_response, meta=meta)

    def parse_performance_response(self, response):
        items = response.meta['items']
        response_jsn = json.loads(response.text)
        fund_data = response_jsn.get("funddata")
        macros = fund_data['Macros']
        macros = {m['Name']: m['Value'].split("T")[0] for m in macros}
        if fund_data:
            fund_navs = fund_data.get("fundNavs", [])
            for item in items:
                fund_nav = [f for f in fund_navs if f['ShareClass'] == item['share_class']]
                if fund_nav:
                    item['total_net_assets'] = "${}".format(round(fund_nav[0].get("TotalNetAssets")))
                    item['total_net_assets_date'] = macros['NAVasOfDateD']

            fund_expenses = fund_data.get("FundExpenses", [])
            for item in items:
                fund_expense = [f for f in fund_expenses if f['CUSIP'] == item['cusip']]
                if fund_expense:
                    fund_expense = fund_expense[0]
                    item['maximum_sales_charge_full_load'] = fund_expense.get("SalesCharge")
                    item['total_expense_gross'] = fund_expense.get("GrossOperatingExpenses")
                    item['total_expense_net'] = fund_expense.get("NetOperatingExpenses")
                yield item

