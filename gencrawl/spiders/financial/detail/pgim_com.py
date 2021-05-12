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
        for item in items:
            item['instrument_name'] = fund_data

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

        fund_profiles = fund_data.get("FundProfile")
        for item in items:
            fund_profile = [f for f in fund_profiles if f.get("ReportFundClass", {}).get("CUSIP") == item['cusip']]
            if fund_profile:
                fund_profile = fund_profile[0]['ReportFundClass']
                item['share_inception_date'] = fund_profile.get("InceptionDate").split("T")[0]
                item['instrument_name'] = fund_profile.get("Name")

        common_data = response_jsn.get("common", {}).get("CommonText")
        if common_data:
            fund_managers = []
            for c in common_data:
                if c.get("LocationName") == "Manager Tab -  Picture and Bio":
                    print(c)
                else:
                    print(c.get("LocationName") + "xxx")
            managers = [c for c in common_data if c.get("LocationName") == "Manager Tab -  Picture and Bio"]
            for m in managers:
                fund_managers.append({"fund_manager": m.get("ShortName", "").split("-")[0].strip()})
            for item in items:
                item['fund_managers'] = fund_managers

        for item in items:
            yield item

