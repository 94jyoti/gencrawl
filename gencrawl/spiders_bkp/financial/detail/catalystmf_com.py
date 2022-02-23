from gencrawl.spiders.financial.financial_detail_spider import FinancialDetailSpider
from gencrawl.spiders.financial.financial_detail_field_mapping import FinancialDetailFieldMapSpider
import scrapy
import re
import pandas as pd


class CatalystmfComDetail(FinancialDetailFieldMapSpider):
    name = 'financial_detail_catalystmf_com'

    def get_items_or_req(self, response, default_item=None):
        items = super().get_items_or_req(response, default_item)
        fund_managers_list = []
        data_dict = {"fund_manager": "", "fund_manager_years_of_experience_in_industry": "",
                     "fund_manager_firm": "", "fund_manager_years_of_experience_with_fund": ""}
        if (items[0]['fund_managers'] == []):
            print("inside iffffffff")
            if(response.xpath("//strong[contains(text(), 'Portfolio Manager')]//following-sibling::text()").extract()):
                temp_fund_manager = response.xpath(
                    "//strong[contains(text(), 'Portfolio Manager')]//following-sibling::text()").extract()
            if(response.xpath("//i[contains(text(), 'Portfolio Manager')]//parent::strong//parent::p/strong/text()").extract()):
                temp_fund_manager = response.xpath("//i[contains(text(), 'Portfolio Manager')]//parent::strong//parent::p/strong/text()").extract()
            if(response.xpath("//div[@id='fundmanagement']/following-sibling::div[last()]//p//strong//text()").extract()):
                temp_fund_manager=response.xpath("//div[@id='fundmanagement']/following-sibling::div[last()]//p//strong//text()").extract()
            if(response.xpath("//span[contains(text(),'Portfolio')]/parent::div/a//span[1]//text()").extract()):
                temp_fund_manager=response.xpath("//span[contains(text(),'Portfolio')]/parent::div/a//span[1]//text()").extract()
            if(response.xpath("//i[contains(text(),'Portfolio Manager')]/parent::strong/preceding-sibling::strong/text()").extract()):
                temp_fund_manager=response.xpath("//i[contains(text(),'Portfolio Manager')]/parent::strong/preceding-sibling::strong/text()").extract()
        else:
            pass
        try:
            for i in range(len(temp_fund_manager)):
                data_dict = {"fund_manager": "", "fund_manager_years_of_experience_in_industry": "",
                             "fund_manager_firm": "", "fund_manager_years_of_experience_with_fund": ""}
                data_dict['fund_manager'] = temp_fund_manager[i]
                fund_managers_list.append(data_dict)
            for i in items:
                i['fund_managers'] = fund_managers_list
                i['fund_managers']=[set(i['fund_managers'])]
                if('Advisor' not in i['portfolio_consultant']):
                	i['portfolio_consultant']=""
                if(('Sub-Advisor') in i['portfolio_consultant']):
                	i['portfolio_consultant']=""
                i['portfolio_consultant']=i['portfolio_consultant'].replace("Investment Advisor:","").replace(":","").strip()
        except:
            fundd_temp=[]
            for i in items:
                for value in i['fund_managers']:
                    if(value not in fundd_temp):
                    	fundd_temp.append(value)
                    else:
                    	continue
                i['fund_managers']=fundd_temp
                if('Advisor' not in i['portfolio_consultant']):
                	i['portfolio_consultant']=""
                if(('Sub-Advisor') in i['portfolio_consultant']):
                	i['portfolio_consultant']=""
                i['portfolio_consultant']=i['portfolio_consultant'].replace("Investment Advisor:","").replace(":","").strip()
            return items

        return items