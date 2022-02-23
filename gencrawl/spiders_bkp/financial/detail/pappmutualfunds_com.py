from gencrawl.spiders.financial.financial_detail_spider import FinancialDetailSpider
from gencrawl.spiders.financial.financial_detail_field_mapping import FinancialDetailFieldMapSpider
import scrapy


class PappmutualfundsComDetail(FinancialDetailFieldMapSpider):
    name = 'financial_detail_pappmutualfunds_com'

    def get_items_or_req(self, response, default_item=None):
        
        items = super().get_items_or_req(response, default_item)
        home_page_url = 'https://www.pappmutualfunds.com/' + response.xpath(\
                                "//a[contains(text(),'ABOUT US')]/@href").extract()[0]
        meta = response.meta
        meta['items'] = items
        resp = self.make_request(home_page_url, callback=self.parse_fund_manager, meta=meta)
        return resp


    def parse_fund_manager(self, response):
        '''
        Extracting multiple fund_managers from About us tab.
        url:- https://www.pappmutualfunds.com/team.html
        '''

        fund_manager_list=[]
        items = response.meta['items']
        try:
            temp_fund_mgr_lst = ''.join(response.xpath(\
                            "//p[span[contains(text(),'Portfolio Managers')]]/following-sibling::table[1]//tr/td[2]//td[span[contains(@class,'caps')]]//text()"\
                            ).extract()).split('CFA')
            complete_temp_fund_mgr_lst = [item.strip() + ' CFA' for item in temp_fund_mgr_lst if item.strip() !='']
        except Exception as e:
            complete_temp_fund_mgr_lst = []
        
        for fnd_mgr in complete_temp_fund_mgr_lst:
            data_dict = {'fund_manager':fnd_mgr}
            fund_manager_list.append(data_dict)
        items[0]['fund_managers']=fund_manager_list
        return items
