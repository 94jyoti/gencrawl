from gencrawl.spiders.financial.financial_detail_spider import FinancialDetailSpider
from gencrawl.util.statics import Statics
import json
import scrapy
from gencrawl.items.financial.financial_detail_item import FinancialDetailItem
from datetime import datetime
import datetime
import urllib.parse


class DodgeandcoxComDetail(FinancialDetailSpider):
    name = 'financial_detail_dodgeandcox_com'

    def get_items_or_req(self, response, default_item={}):
        items = self.prepare_items(response, default_item)
        item = items[0]
        api_url = "https://dodgeandcox.com/"+''.join(response.xpath('//span[contains(text(),"Characteristics")]/parent::a/@href').extract())
        meta = response.meta
        meta['items'] = item
        item['api_url'] = api_url
        r = self.make_request(api_url, callback=self.parse_performance_response, meta=meta)
        return r

    def parse_performance_response(self, response):
        items = response.meta['items']

        items['benchmarks'] = ', '.join(response.xpath('//th[contains(normalize-space(text()),"Year") or contains(normalize-space(text()),"SINCE INCEPTION")]/parent::tr/parent::thead/parent::table/tbody/tr[@class="scaled-text"]/td[1]/text()').extract()).strip()
        items['total_net_assets'] = response.xpath('//th[contains(normalize-space(text()),"Total Net Assets")]/following-sibling::td[2]/text()').extract_first()
        items['total_expense_gross'] = response.xpath('//th[contains(normalize-space(text()),"Expense Ratio")]/following-sibling::td[2]/text()').extract_first()
        items['turnover_rate'] = response.xpath('//th[contains(normalize-space(text()),"Portfolio Turnover")]/following-sibling::td[2]/text()').extract_first()
        items['turnover_rate_date'] = response.xpath('//th[contains(normalize-space(text()),"Portfolio Turnover")]/span/text()').extract_first().split(',')[0].replace('(','')
        items['sec_yield_30_day'] = response.xpath('//th[contains(normalize-space(text()),"30-Day SEC")]/following-sibling::td[2]/text()').extract_first()
        items['sec_yield_date_30_day'] = response.xpath('//span[@class="bodycopy scaled-text"]/text()').extract_first().split('\t')[-1].split('(')[0].strip()
        items['effective_duration'] = response.xpath('//td[contains(normalize-space(text()),"Effective Duration")]/following-sibling::td[2]/text()').extract_first()

        yield self.generate_item(items, FinancialDetailItem)
