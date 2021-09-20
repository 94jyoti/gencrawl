from gencrawl.spiders.financial.financial_detail_spider import FinancialDetailSpider
from gencrawl.util.statics import Statics
import json
import scrapy
from gencrawl.items.financial.financial_detail_item import FinancialDetailItem
from datetime import datetime
import datetime
import urllib.parse
from gencrawl.util.statics import Statics


class CommerceComDetail(FinancialDetailSpider):
    name = 'financial_detail_commerce_com'

    def get_items_or_req(self, response, default_item={}):
        items = self.prepare_items(response, default_item)
        main_url = "https://www.commercefunds.com/fund-information/mutual-funds"
        meta = response.meta
        meta['items'] = items
        yield self.make_request(main_url, callback=self.dividends, meta=meta, dont_filter=True,method=Statics.CRAWL_METHOD_SELENIUM)


    def dividends(self, response):
        items = response.meta['items']
        nasdaq_ticker_temp=response.xpath("//tbody//tr")
        for row in nasdaq_ticker_temp:
        	nasdaq_ticker_main=row.xpath(".//td[1]//text()").extract_first()
        	if(items[0]['nasdaq_ticker'].strip()==nasdaq_ticker_main.strip()):
        		items[0]['dividend_frequency']=row.xpath(".//td[4]//text()").extract_first()

        distribution_url = "https://www.commercefunds.com/fund-information/distributions"
        meta = response.meta
        meta['items'] = items
        yield self.make_request(distribution_url, callback=self.parse_distribution, meta=meta, dont_filter=True,method=Statics.CRAWL_METHOD_SELENIUM)


    def parse_distribution(self, response):
        items = response.meta['items']
        dividends = []
        capital_gains = []
        # Logic for Income Distribution
        current_ticker = items[0]['nasdaq_ticker']
        ticker_list = response.xpath("//thead[tr[th[contains(text(),'Ticker')]]]/following-sibling::tbody/tr/td[1]/text()").extract()
        temp_record_date = response.xpath("//h2[contains(text(),'Income Distribution')]/following-sibling::p[1]/strong[1]/following::text()[1]").extract()
        
        for i in range(len(temp_record_date)):
            ticker_block_obj = response.xpath("//h2[contains(text(),'Income Distribution')]/following-sibling::p[1]/following-sibling::div[1]")[i]
            tickers_row = ticker_block_obj.xpath("./table/tbody/tr")
            for each_row in tickers_row:
                ticker = each_row.xpath("./td[1]/text()").extract()[0]
                if ticker == current_ticker:
                    record_date = temp_record_date[i].replace('(close of business)','').strip()
                    ex_date = response.xpath("//h2[contains(text(),'Income Distribution')]/following-sibling::p[1]/strong[2]/following::text()[1]").extract()[i]
                    pay_date = response.xpath("//h2[contains(text(),'Income Distribution')]/following-sibling::p[1]/strong[3]/following::text()[1]").extract()[i]
                    per_share = each_row.xpath("./td[2]/text()").extract()[0]
                    divident_dict = {'ex_date':ex_date, 'pay_date':pay_date,\
                                            'per_share':per_share,\
                                            'record_date':record_date}
                    dividends.append(divident_dict)
        items[0]['dividends'] = dividends
        # Logic for Captial Gains
        fund_name = items[0]['instrument_name'].replace('Fund','').strip()
        fund_block_obj = response.xpath("//h2[contains(text(),'Capital Gains Distribution')]/following-sibling::table[1]/tbody/tr")
        for each_fund in fund_block_obj:
            fund = each_fund.xpath("./th[1]/span/a/text()").extract()[0]
            if fund == fund_name:
                cg_record_date = response.xpath("//h2[contains(text(),'Capital Gains Distribution')]/following-sibling::p[1]/strong[1]/following::text()[1]"\
                                                    ).extract()[0].replace('(close of business)','').strip()
                cg_ex_date = response.xpath("//h2[contains(text(),'Capital Gains Distribution')]/following-sibling::p[1]/strong[2]/following::text()[1]").extract()[0]
                cg_pay_date = response.xpath("//h2[contains(text(),'Capital Gains Distribution')]/following-sibling::p[1]/strong[3]/following::text()[1]").extract()[0]
                cg_short_term_per_share = each_fund.xpath("./td[1]/text()").extract()[0]
                cg_long_term_per_share = each_fund.xpath("./td[2]/text()").extract()[0]
                capital_gains_dict = {'cg_ex_date':cg_ex_date, 'cg_pay_date':cg_pay_date,\
                                    'short_term_per_share':cg_short_term_per_share,\
                                    'long_term_per_share':cg_long_term_per_share,\
                                    'cg_record_date':cg_record_date}
                capital_gains.append(capital_gains_dict)
        items[0]['capital_gains'] = capital_gains
        
        yield self.generate_item(items[0], FinancialDetailItem)