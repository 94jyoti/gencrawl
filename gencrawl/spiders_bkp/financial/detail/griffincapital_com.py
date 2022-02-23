from gencrawl.spiders.financial.financial_detail_spider import FinancialDetailSpider
from gencrawl.spiders.financial.financial_detail_field_mapping import FinancialDetailFieldMapSpider
import scrapy


class GriffincapitalComDetail(FinancialDetailSpider):
    name = 'financial_detail_griffincapital_com'

    def get_items_or_req(self, response, default_item=None):
        items = super().get_items_or_req(response, default_item)
        # fund_mgr_page_url = 'https://www.griffincapital.com/griffin-institutional-access-credit-fund/about/griffin-capital-team/'
        try:
            fund_mgr_page_url = response.xpath("//a[contains(text(),'Griffin Capital Team')]/@href").extract()[0]
        except:
            fund_mgr_page_url = response.xpath("//a[contains(text(),'Executive Management')]/@href").extract()[0]
        meta = response.meta
        meta['items'] = items
        resp = self.make_request(fund_mgr_page_url, callback=self.parse_fund_manager, meta=meta)
        return resp


    def parse_fund_manager(self, response):
        fund_manager_list=[]
        items = response.meta['items']
        try:
            temp_fund_mgr_lst = response.xpath(\
                            "//div[@class = 'name']/text()"\
                            ).extract()
        except Exception as e:
            temp_fund_mgr_lst = []
        
        for fnd_mgr in temp_fund_mgr_lst:
            data_dict = {'fund_manager':fnd_mgr}
            fund_manager_list.append(data_dict)
        items[0]['fund_managers'] = fund_manager_list
        return items
