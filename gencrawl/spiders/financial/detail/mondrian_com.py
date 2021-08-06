from gencrawl.spiders.financial.financial_detail_spider import FinancialDetailSpider
from gencrawl.util.statics import Statics
import json
import scrapy
from gencrawl.items.financial.financial_detail_item import FinancialDetailItem
from datetime import datetime
import datetime
import re
class MondrianComDetail(FinancialDetailSpider):
    name = 'financial_detail_mondrian_com'

    def get_items_or_req(self, response, default_item={}):
        items = self.prepare_items(response, default_item)
        #item=items[0]
        try:
        	fund_manager_url=response.xpath('//a[@title="Bio"]//@href').extract()
        	for i in range(len(fund_manager_url)):
        		fund_manager_url[i]=items[0]['fund_url']+fund_manager_url[i]
        	meta = response.meta
        	items[0]['temp_manager']=fund_manager_url[1:]
        	items[0]['temp_fund_manager_list']=[]
        	meta['items'] = items
        	items[0]['main_url']=fund_manager_url[0]
        	print("first_functuon",items[0]['main_url'])
        	yield self.make_request(items[0]['main_url'], callback=self.fund_manager, meta=meta, dont_filter=True)
        except:
        	yield self.generate_item(items[0], FinancialDetailItem)	
        	
    def fund_manager(self, response):
        file=open("mondrian.html","w")
        file.write(response.text)
        file.close()
        items = response.meta['items']
        print("second function main urllll",items[0]['main_url'])
        print(response.xpath("//h2[contains(text(),'Years')]//ancestor::div[@class='elementor-widget-wrap'][2]//div[contains(@data-widget_type,'heading.default')][1]//h2//text()").extract())
        fund_manager_list=[]
        fund_manager_temp=response.xpath("//h2[contains(text(),'Years')]//ancestor::div[@class='elementor-widget-wrap'][2]//div[contains(@data-widget_type,'heading.default')][1]//h2//text()").extract()
        temp=[fund_manager_temp[i:i + 3] for i in range(0, len(fund_manager_temp), 3)]
        for i in range(len(temp)):
        	data_dict={"fund_manager": "","fund_manager_years_of_experience_in_industry":"","fund_manager_years_of_experience_with_fund": ""}
        	
        	data_dict['fund_manager']=temp[i][0]
        	print("data dict",data_dict)
        	data_dict['fund_manager_years_of_experience_in_industry']=temp[i][2]
        	data_dict['fund_manager_years_of_experience_with_fund']=temp[i][1]
        	fund_manager_list.append(data_dict)
        	meta = response.meta
        	meta['items'] = items
        items[0]['fund_managers']=fund_manager_list
        yield self.generate_item(items[0], FinancialDetailItem)        	
        
        
        '''
        fund_manager_temp=response.xpath("//h2[contains(text(),'Portfolio')]//preceding::h2[1]//text()").extract()
        experience_with_fund=[]
        print("dvdv ddvdvdvddvdvdcdscdscdsc",response.xpath("//h2[contains(text(),'Portfolio')]//parent::div//following::section//h2//text()").extract())
        for i in response.xpath("//h2[contains(text(),'Portfolio')]//parent::div//following::section//h2//text()").extract():
        	years=re.findall(r'\d+', i)
        	if(len(years)!=0):
        		experience_with_fund.append(years[0])
        print(experience_with_fund)
        #divide list into 2
        fund_experience=[experience_with_fund[i:i + 2] for i in range(0, len(experience_with_fund), 2)][0]
        industry_experience=[experience_with_fund[i:i + 2] for i in range(0, len(experience_with_fund), 2)][1]
        fund_manager_list=[]
        for i in range(len(fund_manager_temp)-1):
        #[{"fund_manager": "", "fund_manager_years_of_experience_in_industry": "", "fund_manager_firm": "",
    # "fund_manager_years_of_experience_with_fund": ""}]	
        #if(len(items[0]['main_url'])!=0):
        	data_dict={"fund_manager": "","fund_manager_years_of_experience_in_industry":"","fund_manager_years_of_experience_with_fund": ""}
        	
        	data_dict['fund_manager']=fund_manager_temp[i]
        	print("data dict",data_dict)
        	data_dict['fund_manager_years_of_experience_in_industry']=industry_experience[i]
        	data_dict['fund_manager_years_of_experience_with_fund']=fund_experience[i]
        	fund_manager_list.append(data_dict)
        	meta = response.meta
        	meta['items'] = items
        items[0]['fund_managers']=fund_manager_list
        yield self.generate_item(items[0], FinancialDetailItem)
        '''		