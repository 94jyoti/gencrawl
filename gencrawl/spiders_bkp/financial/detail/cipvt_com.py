from gencrawl.spiders.financial.financial_detail_spider import FinancialDetailSpider
from gencrawl.spiders.financial.financial_detail_field_mapping import FinancialDetailFieldMapSpider
import scrapy


class CipvtComDetail(FinancialDetailSpider):
    name = 'financial_detail_cipvt_com'

    def get_items_or_req(self, response, default_item=None):
        items = super().get_items_or_req(response, default_item)
        import pdb;pdb.set_trace()
        fund_mgr_page_url = response.xpath(\
                            "//ul[@class='investments-nav my-3']//a[text()='Team']/@href"\
                            ).extract()[0]
        share_class_list = response.xpath("//div[contains(@id,'shares')]/preceding-sibling::div[1]/a[contains(text(),'Shares')]/text()"\
                                            ).extract()
        for i in range(len(items)):
            items[i]['share_class'] = share_class_list[i].strip()
        meta = response.meta
        meta['items'] = items
        resp = self.make_request(fund_mgr_page_url, callback=self.parse_fund_manager, method='SELENIUM', meta=meta)
        return resp


    def parse_fund_manager(self, response):
        fund_manager_list=[]
        items = response.meta['items']
        try:
            temp_fund_mgr_lst = response.xpath(\
                            "//span[@class = 'name']/text()"\
                            ).extract()
        except Exception as e:
            temp_fund_mgr_lst = []
        
        for fnd_mgr in temp_fund_mgr_lst:
            data_dict = {'fund_manager':fnd_mgr}
            fund_manager_list.append(data_dict)
        
        for i in range(len(items)):
            items[i]['fund_managers'] = fund_manager_list
        return items

