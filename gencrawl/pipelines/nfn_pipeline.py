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
        self.all_fields ={"fund_url":"fund_url","api_url":"api_url","instrument_name":"instrument_name","nasdaq_ticker":"nasdaq_ticker","cusip":"cusip","isin":"isin","share_class":"share_class","asset_class":"asset_class","portfolio_management_style":"portfolio_management_style","weighting_method":"weighting_method","portfolio_consultant":"portfolio_consultant","portfolio_assets":"portfolio_assets","portfolio_assets_date":"portfolio_assets_date","total_net_assets":"total_net_assets","total_net_assets_date":"total_net_assets_date","number_of_shareholders":"number_of_shareholders","number_of_shareholders_date":"number_of_shareholders_date","total_shares_outstanding":"total_shares_outstanding","total_shares_outstanding_date":"total_shares_outstanding_date","annual_fund_operating_expenses_after_fee_waiver":"annual_fund_operating_expenses_after_fee_waiver","fees_total_12b_1":"fees_total_12b_1","other_expenses":"other_expenses","management_fee":"management_fee","shareholder_service_fees":"shareholder_service_fees","initial_sales_charge":"initial_sales_charge","deferred_sales_charge":"deferred_sales_charge","contingent_deferred_sales_charge":"contingent_deferred_sales_charge","redemption_fee":"redemption_fee","exchange_fee":"exchange_fee","account_fee":"account_fee","purchase_fee":"purchase_fee","expense_waivers":"expense_waivers","management_fee_maximum":"management_fee_maximum","maximum_sales_charge_full_load":"maximum_sales_charge_full_load","dividend_expense_on_securities":"dividend_expense_on_securities","remainder_of_other_expenses":"remainder_of_other_expenses","total_expense_gross":"total_expense_gross","total_expense_net":"total_expense_net","acquired_fund_fees_and_expenses":"acquired_fund_fees_and_expenses","share_inception_date":"share_inception_date","investment_objective":"investment_objective","investment_strategy":"investment_strategy","duration":"duration","duration_as_of_date":"duration_as_of_date","effective_duration":"effective_duration","effective_duration_date":"effective_duration_date","weighted_average_duration":"weighted_average_duration","weighted_average_duration_as_of_date":"weighted_average_duration_as_of_date","average_effective_duration":"average_effective_duration","average_effective_duration_as_of_date":"average_effective_duration_as_of_date","average_modified_duration":"average_modified_duration","average_weighted_maturity":"average_weighted_maturity","average_weighted_maturity_as_of_date":"average_weighted_maturity_as_of_date","average_weighted_effective_maturity":"average_weighted_effective_maturity","average_weighted_effective_maturity_as_of_date":"average_weighted_effective_maturity_as_of_date","average_effective_maturity":"average_effective_maturity","average_effective_maturity_as_of_date":"average_effective_maturity_as_of_date","minimum_initial_investment":"minimum_initial_investment","minimum_additional_investment":"minimum_additional_investment","turnover_rate":"turnover_rate","turnover_rate_date":"turnover_rate_date","sub_advisor":"sub_advisor","management_process":"management_process","fund_distribution_type":"fund_distribution_type","distribution_frequency":"distribution_frequency","dividend_frequency":"dividend_frequency","sec_yield_30_day":"sec_yield_30_day","sec_yield_date_30_day":"sec_yield_date_30_day","sec_yield_without_waivers_30_day":"sec_yield_without_waivers_30_day","sec_yield_without_waivers_date_30_day":"sec_yield_without_waivers_date_30_day","sec_yield":"sec_yield","sec_yield_date":"sec_yield_date","sector_allocation":"sector_allocation","sector_allocation_date":"sector_allocation_date","regional_diversification":"regional_diversification","regional_diversification_date":"regional_diversification_date","country_diversification":"country_diversification","country_diversification_date":"country_diversification_date","yields":"yields","sec_yield_7_day":"sec_yield_7_day","sec_yield_date_7_day":"sec_yield_date_7_day","effective_yield_7_day":"effective_yield_7_day","effective_yield_date_7_day":"effective_yield_date_7_day","current_yield_7_day":"current_yield_7_day","current_yield_date_7_day":"current_yield_date_7_day","distribution_yield_12_month":"distribution_yield_12_month","footnote_symbol":"footnote_symbol","footnote":"footnote","benchmarks":"benchmarks","capital_gains":"capital_gains","cg_ex_date":"cg_ex_date","cg_record_date":"cg_record_date","cg_pay_date":"cg_pay_date","cg_reinvestment_price":"cg_reinvestment_price","short_term_per_share":"short_term_per_share","long_term_per_share":"long_term_per_share","total_per_share":"total_per_share","dividends":"dividends","ex_date":"ex_date","record_date":"record_date","pay_date":"pay_date","ordinary_income":"ordinary_income","qualified_income":"qualified_income","per_share":"per_share","reinvestment_price":"reinvestment_price","fund_managers":"fund_managers","fund_manager":"fund_manager","fund_manager_years_of_experience_in_industry":"fund_manager_years_of_experience_in_industry","fund_manager_firm":"fund_manager_firm","fund_manager_years_of_experience_with_fund":"fund_manager_years_of_experience_with_fund","average_duration":"average_duration","average_duration_as_of_date":"average_duration_as_of_date","website":"website","crawl_datetime":"crawl_datetime","http_status":"http_status","job_id":"job_id","gencrawl_id":"gencrawl_id"}
        self.field_mapping = self.all_fields
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
        #for row in Utility.read_csv(field_mapping_file):
         #   self.field_mapping[row['key']] = row['value']

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
