# -*- coding: utf-8 -*-

# Product item class.
# will be generated from product detail pages

from scrapy import Field
from gencrawl.items.financial import FinancialItem


class FinancialDetailItem(FinancialItem):
    total_net_assets = Field()
    turnover_rate = Field()
    total_net_assets_date = Field()
    turnover_rate_date = Field()
    total_expense_gross = Field()
    total_expense_net = Field()
    share_inception_date = Field()
    sector_allocation = Field()
    sector_allocation_date = Field()
    country_diversification = Field()
    country_diversification_date = Field()
    isin = Field()
    asset_class = Field()
    portfolio_management_style = Field()
    weighting_method = Field()
    portfolio_consultant = Field()
    portfolio_assets = Field()
    portfolio_assets_date = Field()
    number_of_shareholders = Field()
    number_of_shareholders_date = Field()
    total_shares_outstanding = Field()
    total_shares_outstanding_date = Field()
    annual_fund_operating_expenses_after_fee_waiver = Field()
    other_expenses = Field()
    management_fee = Field()
    shareholder_service_fees = Field()
    initial_sales_charge = Field()
    deferred_sales_charge = Field()
    contingent_deferred_sales_charge = Field()
    redemption_fee = Field()
    exchange_fee = Field()
    account_fee = Field()
    purchase_fee = Field()
    expense_waivers = Field()
    management_fee_maximum = Field()
    maximum_sales_charge_full_load = Field()
    dividend_expense_on_securities = Field()
    remainder_of_other_expenses = Field()
    acquired_fund_fees_and_expenses = Field()
    investment_objective = Field()
    investment_strategy = Field()
    duration = Field()
    duration_as_of_date = Field()
    average_modified_duration = Field()
    average_weighted_maturity = Field()
    average_weighted_maturity_as_of_date = Field()
    average_weighted_effective_maturity = Field()
    average_weighted_effective_maturity_as_of_date = Field()
    minimum_initial_investment = Field()
    minimum_additional_investment = Field()
    management_process = Field()
    fund_distribution_type = Field()
    distribution_frequency = Field()
    dividend_frequency = Field()
    yields = Field()
    sec_yield = Field()
    sec_yield_date = Field()
    regional_diversification = Field()
    regional_diversification_date = Field()
    footnote_symbol = Field()
    footnote = Field()
    effective_duration = Field()
    effective_duration_date = Field()
    
    #added below two fields by @Jyoti 
    weighted_average_duration = Field()
    weighted_average_duration_as_of_date = Field()
    average_effective_duration = Field()
    average_effective_duration_as_of_date = Field()
    api_url = Field()
    # ["Benchmark 1", ""Benchmark 2"]
    benchmarks = Field()

    # [{"ex_date": "", "record_date": "", "pay_date": "", "short_term_per_share": "", "long_term_per_share": "",
    # "total_per_share": "", "reinvestment_price": ""}]
    capital_gains = Field()

    # [{"ex_date": "", "pay_date": "", "ordinary_income": "", "qualified_income": "", "record_date": "",
    # "per_share": "", "reinvestment_price": ""}]
    dividends = Field()

    # [{"fund_manager": "", "fund_manager_years_of_experience_in_industry": "", "fund_manager_firm": "",
    # "fund_manager_years_of_experience_with_fund": ""}]
    fund_managers = Field()

    fees_total_12b_1 = Field()
    sub_advisor = Field()
    sec_yield_7_day = Field()
    sec_yield_date_7_day = Field()
    effective_yield_7_day = Field()
    effective_yield_date_7_day = Field()
    current_yield_7_day = Field()
    current_yield_date_7_day = Field()
    sec_yield_without_waivers_30_day = Field()
    sec_yield_without_waivers_date_30_day = Field()
    sec_yield_30_day = Field()
    sec_yield_date_30_day = Field()
    distribution_yield_12_month = Field()



