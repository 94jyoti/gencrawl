from gencrawl.spiders.financial.financial_detail_spider import FinancialDetailSpider
from gencrawl.spiders.financial.financial_detail_field_mapping import FinancialDetailFieldMapSpider
import scrapy


class HwcmComDetail(FinancialDetailFieldMapSpider):
    name = 'financial_detail_hwcm_com'

    def get_items_or_req(self, response, default_item=None):
        items = super().get_items_or_req(response, default_item)
        mgmt_fee_page_url = response.url.replace('summary','expenses/#skip_tabs')
        meta = response.meta
        meta['items'] = items
        resp = self.make_request(mgmt_fee_page_url, callback=self.parse_mgmt_fee, meta=meta)
        return resp


    def parse_mgmt_fee(self, response):
        items = response.meta['items']
        try:
            mgmt_fee = response.xpath(\
                            "//td[text()='Management Fee']/following-sibling::td[1]/text()"\
                            ).extract()[0]

            twelve_b1 = response.xpath(\
                            "//td[text()='12b-1 Fee']/following-sibling::td[1]/text()"\
                            ).extract()[0]

            minimum_additional_investment = response.xpath(\
                            "//td[text()='Minimum Subsequent Investment']/following-sibling::td[1]/text()"\
                            ).extract()[0]
            try:
                cont_deffered_sales = response.xpath(\
                                "//th[contains(text(),'CONTINGENT')]/following::tr[1]/td[2]/text()"\
                                ).extract()[0]
            except:
                cont_deffered_sales = ''

            try:
                initial_sales_charge = response.xpath(\
                                "//tr[th[contains(text(),'FRONT-END SALES CHARGE')]]/following-sibling::tr[1]/td[2]/text()"\
                                ).extract()[0]
            except:
                initial_sales_charge = ''
                
                            
        except Exception as e:
            mgmt_fee = ''
            twelve_b1 = ''
            minimum_additional_investment = ''
            
        
        items[0]['management_fee'] = mgmt_fee
        items[0]['fees_total_12b_1'] = twelve_b1
        items[0]['minimum_additional_investment'] = minimum_additional_investment
        items[0]['contingent_deferred_sales_charge'] = cont_deffered_sales
        items[0]['initial_sales_charge'] = initial_sales_charge
        # again adding items to meta and sending to another connector:- Multiple connectors
        meta = response.meta
        meta['items'] = items
        benchmark_url = response.url.replace('expenses','performance')
        
        resp2 = self.make_request(benchmark_url, callback=self.parse_benchmarks, meta=meta)
        yield resp2

    def parse_benchmarks(self, response):
        items = response.meta['items']
        benchmark_list = response.xpath("//div[contains(@class,'table__perf-month-')]//td[contains(text(),'Index')]/text() ").extract()
        items[0]['benchmarks'] = benchmark_list
        return items