from gencrawl.spiders.financial.financial_detail_spider import FinancialDetailSpider
from gencrawl.spiders.financial.financial_detail_field_mapping import FinancialDetailFieldMapSpider
import scrapy
import re
import json
import pandas as pd
from gencrawl.items.financial.financial_detail_item import FinancialDetailItem
class FeimComDetail(FinancialDetailFieldMapSpider):
    name = 'financial_detail_feim_com'

    def get_items_or_req(self, response, default_item=None):
        items = super().get_items_or_req(response, default_item)
        file=open("fiem.html","w")
        file.write(response.text)
        file.close()
        for item in items:
            if(item['minimum_initial_investment']==[]):
                temp_investment=response.xpath('//td[contains(text(),"Minimum Investment")]/text()').extract()
                temp_investment=[i.replace("Minimum Investment - Class",'').strip() for i in temp_investment]
                counter=-1
                for item_invest in temp_investment:
                    counter=counter+1
                    if(item['share_class'] in item_invest):
                        item['minimum_initial_investment']=response.xpath('//td[contains(text(),"Minimum Investment")]/following-sibling::td//text()').extract()[counter]
            #minimum addition investment
            if(item['minimum_additional_investment']==[]):
                temp_min_investment=response.xpath('//td[contains(text(),"Subsequent Investment")]/text()').extract()
                temp_min_investment=[i.replace("Subsequent Investment - Class",'').strip() for i in temp_min_investment]
                counter=-1
                for item_invest in temp_min_investment:
                    counter=counter+1
                    if(item['share_class'] in item_invest):
                        item['minimum_additional_investment']=response.xpath('//td[contains(text(),"Subsequent Investment")]/following-sibling::td//text()').extract()[counter]

        data=re.findall('Drupal\.settings,(.*?)></script>',response.text.replace("\n",""))[0].replace(");//--><!]]","")
        json_data=json.loads(data)
        node_value= list(json_data['charts'])[-1]
        distribution_data=json_data['charts'][node_value]
        ticker_list=[]
        for ticker in distribution_data['data_info']['legends'].keys():
            ticker_list.append(ticker)

        for item in range(len(items)):
            dict_key=ticker_list[item]
            capital_gain_list=[]
            dividend_list=[]
            #final=item[dict_key]

            cg_data=distribution_data['data_info']['data'][dict_key]
            for i in cg_data.values():
                for j in i.values():
                    data_dict1 = {"ex_date": "", "pay_date": "", "ordinary_income": "", "qualified_income": "","record_date": "", "per_share": "", "reinvestment_price": ""}
                    data_dict2 = {'long_term_per_share': "", 'cg_ex_date': "", 'cg_record_date': "", 'cg_pay_date': "",'short_term_per_share': "", 'total_per_share': "", 'cg_reinvestment_price': ""}
                    data_dict1['record_date']=j['column_0']
                    data_dict1['ex_date']=j['column_1']
                    data_dict1['pay_date']=j['column_2']
                    data_dict1['ordinary_income']=j['column_3']
                    data_dict2['short_term_per_share']=j['column_4']
                    data_dict2['long_term_per_share']=j['column_5']
                    capital_gain_list.append(data_dict2)
                    dividend_list.append(data_dict1)
            items[item]['capital_gains']=capital_gain_list
            items[item]['dividends']=dividend_list
            yield self.generate_item(items[item], FinancialDetailItem)




        #return items