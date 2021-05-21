from gencrawl.spiders.financial.financial_detail_spider import FinancialDetailSpider
from gencrawl.util.statics import Statics
import json


class PgimComDetail(FinancialDetailSpider):
    name = 'financial_detail_pgim_com'
    performance_api = "https://www.pgim.com/pcom6/services/pcom/reportjson?&pageid=1&fundname={fund_name}&fundid=undefined"
    capital_gains_api = "https://www.pgim.com/pcom6/services/pcom/reportjson?pageid=8&fundname={}&fundid={}"

    def parse_navigation(self, response, items):
        fund_name = response.request.url.split("/")[-1]
        performance_api = self.performance_api.format(fund_name=fund_name)
        meta = response.meta
        meta['items'] = items
        meta['fund_name'] = fund_name
        return self.make_request(performance_api, callback=self.parse_performance_response, meta=meta)

    def parse_performance_response(self, response):
        items = response.meta['items']
        response_jsn = json.loads(response.text)
        fund_data = response_jsn.get("funddata")
        macros = fund_data['Macros']
        macros = {m['Name']: m['Value'].split("T")[0] for m in macros}
        fund_navs = fund_data.get("fundNavs", [])
        for item in items:
            fund_nav = [f for f in fund_navs if f['ShareClass'] == item['share_class']]
            if fund_nav:
                fund_nav = fund_nav[0]
                item['total_net_assets'] = "${}".format(round(fund_nav.get("TotalNetAssets")))
                item['total_net_assets_date'] = macros['NAVasOfDateD']
                item['sec_yield_30_day'] = fund_nav['a30DaySECYieldPercentage']
                item['sec_yield_date_30_day'] = macros['MonthlyYieldDate']
                item['sec_yield_without_waivers_30_day'] = fund_nav['a30DayUnsbSECYieldPercentage']
                item['sec_yield_without_waivers_date_30_day'] = macros['MonthlyYieldDate']

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

        common_data = response_jsn.get("common", {}).get("CommonText")
        if common_data:
            fund_managers = []
            managers = [c for c in common_data if c.get("LocationName") == "Manager Tab -  Picture and Bio"]
            for m in managers:
                fm = m.get("ShortName", "").split("-")[0].strip().split("_Revised")[0]
                fund_managers.append({"fund_manager": fm})
            for item in items:
                item['fund_managers'] = fund_managers

        fund_name = response.meta['fund_name']
        dividend_url = self.capital_gains_api.format(fund_name, fund_name)
        meta = response.meta
        meta['items'] = items
        yield self.make_request(dividend_url, callback=self.parse_capital_gains, meta=meta, dont_filter=True)

    def parse_capital_gains(self, response):
        items = response.meta['items']
        response_jsn = json.loads(response.text)
        if response_jsn.get("Benchmarks"):
            for item in items:
                item['benchmarks'] = response_jsn['Benchmarks']

        fund_data = response_jsn['funddata']
        dividends = fund_data['RegularDividends']
        special_dividends = fund_data['SpecialDividends']
        for item in items:
            parsed_divs = []
            divs = [d for d in dividends if d['ShareClassName'] == item['share_class']]
            special_div = [d for d in special_dividends if d['ShareClassName'] == item['share_class']]
            special_div = {f'{v["RecordDate"]}-{v["PayableDate"]}': v['DataValue'] for v in special_div}
            for div in divs:
                pdiv = dict()
                pdiv['record_date'] = div.get("RecordDate")
                pdiv['pay_date'] = div.get("PayableDate") if div.get("PayableDate") != '01/01/1900' else None
                key = f'{div["RecordDate"]}-{div["PayableDate"]}'
                if special_div.get(key):
                    pdiv['qualified_income'] = special_div[key]
                pdiv['ordinary_income'] = round(div.get("DataValue"), 4)
                pdiv['reinvestment_price'] = div["ReinvestNAV"] if (div.get(
                    "ReinvestNAV") and div['ReinvestNAV'] >= 0) else None
                parsed_divs.append(pdiv)
            item['dividends'] = parsed_divs

        for item in items:
            capital_gains = []
            for short_term, long_term in zip(fund_data['STCapitalGain'], fund_data['LTCapitalGain']):
                if short_term['ShareClassName'] == item['share_class']:
                    capital = dict()
                    capital['cg_ex_date'] = short_term['RecordDate']
                    capital['cg_pay_date'] = short_term['PayableDate'] if short_term.get("PayableDate") != '01/01/1900' else None
                    capital['short_term_per_share'] = short_term['DataValue']
                    capital['long_term_per_share'] = long_term['DataValue']
                    capital['cg_reinvestment_price'] = short_term['ReinvestNAV'] if short_term['ReinvestNAV'] >= 0 else None
                    capital_gains.append(capital)
            item['capital_gains'] = capital_gains
            yield item



