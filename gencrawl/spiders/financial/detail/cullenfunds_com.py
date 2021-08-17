from gencrawl.spiders.financial.financial_detail_spider import FinancialDetailSpider
from gencrawl.util.statics import Statics
import json
import scrapy
from gencrawl.items.financial.financial_detail_item import FinancialDetailItem
from gencrawl.spiders.financial.financial_detail_field_mapping import FinancialDetailFieldMapSpider

from datetime import datetime
import datetime
import urllib.parse
import re
from gencrawl.util.statics import Statics
# import urllib
import itertools
import traceback

from copy import deepcopy

class CullenComDetail(FinancialDetailFieldMapSpider):
    name = 'financial_detail_cullen_com'
    custom_settings = {
        "HTTPCACHE_ENABLED": True,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 2,
        "DOWNLOAD_DELAY": 4,
        "COOKIES_ENABLED": True
    }


    def get_items_or_req(self, response, default_item={}):
        items = super().get_items_or_req(response, default_item)
        # items = self.prepare_mapped_items(response, default_item)
        #print(items)
        dividends_url = "http://www.cullenfunds.com/" + \
                        response.xpath("//a[@id='subNavIcon-dividends']//@href").extract()[0].replace("..", "")
        #print("dividends urllll", dividends_url)
        hit_url = response.xpath('//*[@id="getDividendByYearSelect"]//option//@value').extract()
        meta = response.meta
        meta['items'] = items
        for i in items:
            i['capital_gains'] = []
            i['dividends'] = []
            #print(i['capital_gains'])
        yield self.make_request(dividends_url, callback=self.dividends, meta=meta, method=Statics.CRAWL_METHOD_GET,
                                dont_filter=True)

    def dividends(self, response):
        items = response.meta['items']
        #print("yuyuyuyuyuyuyuyyuyuyuyuuyuyuui",response.text)
        file = open("rsttttttt.html", "w")
        file.write(response.text)
        file.close()
        no_of_years = response.meta.get('no_of_years')
        resource_ids = response.meta.get('resource_ids')
        #print("done")
        no_of_items = len(items)
        distribution_list = []
        capital_gain_list = []
        if (response.xpath("//select[@id='getDividendByYearSelect']//option//text()").extract() != []):
            resource_ids_temp=str(response.xpath("//script//text()[1]").extract()[0].replace("var websiteGlobalJavascriptData =","").replace(";",""))
            resource_ids=json.loads(resource_ids_temp)['resourceIDs']
            no_of_years = response.xpath("//select[@id='getDividendByYearSelect']//option//text()").extract()
        else:
            print("nothing")
        table_distributions = response.xpath("//table[@class='distributions']//tbody//tr")
        len_distribution = len(response.xpath("//table[@class='distributions']//tbody//tr//td[1]").extract())
        divided_length = int(len_distribution / no_of_items)
        for row in table_distributions:
            data_dict_capital = {"cg_ex_date": "", "cg_record_date": "", "cg_pay_date": "", "short_term_per_share": "",
                             "long_term_per_share": "", "total_per_share": "", "cg_reinvestment_price": ""}
            data_dict_dividend = {"ex_date": "", "pay_date": "", "ordinary_income": "", "qualified_income": "",
                              "record_date": "", "per_share": "", "reinvestment_price": ""}
            data_dict_capital['cg_record_date'] = row.xpath('.//td[1]//text()').extract_first()
            if(data_dict_capital['cg_record_date']==None):
            	continue
            else:
            	data_dict_capital['cg_record_date'] = row.xpath('.//td[1]//text()').extract_first()
            	year_of_current_distributions = data_dict_capital['cg_record_date'].split("/")[-1]
            	data_dict_dividend['record_date'] = row.xpath('.//td[1]//text()').extract_first()
            	data_dict_capital['cg_ex_date'] = row.xpath('.//td[2]//text()').extract_first()
            	data_dict_dividend['ex_date'] = row.xpath('.//td[2]//text()').extract_first()
            	data_dict_dividend['ordinary_income'] = row.xpath('.//td[3]//text()').extract_first()
            	data_dict_capital['short_term_per_share'] = row.xpath('.//td[4]//text()').extract_first()
            	data_dict_capital['long_term_per_share'] = row.xpath('.//td[5]//text()').extract_first()
            	data_dict_capital['cg_reinvestment_price'] = row.xpath('.//td[6]//text()').extract_first()
            	data_dict_dividend['reinvestment_price'] = row.xpath('.//td[6]//text()').extract_first()
            	distribution_list.append(data_dict_dividend)
            	capital_gain_list.append(data_dict_capital)
        for item in range(len(items)):
            if (item == 0):
                items[item]['capital_gains'].append(capital_gain_list[0:divided_length])
                items[item]['dividends'].append(distribution_list[0:divided_length])
            elif (item > 1 and item < len(items)):
                increment_division = divided_length + divided_length
                items[item]['capital_gains'].append(capital_gain_list[divided_length:increment_division])
                items[item]['dividends'].append(distribution_list[divided_length:increment_division])
            else:
                increment_division = divided_length + divided_length
                items[item]['capital_gains'].append(capital_gain_list[divided_length:])
                items[item]['dividends'].append(distribution_list[divided_length:])
        meta = response.meta
        try:
            if (year_of_current_distributions in no_of_years):
                no_of_years.remove(year_of_current_distributions)
            #print(no_of_years)
            print("respooo",resource_ids)
            year_to_be_processed = no_of_years[0]
            meta['items'] = items
            headers = {'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36' ,'Content-type': 'application/x-www-form-urlencoded','Accept': '*/*','Origin': 'http://www.cullenfunds.com','Referer': 'http://www.cullenfunds.com/mutual-funds/high-dividend/dividends','Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8'}
            #meta['resource_ids']=deepcopy(resource_ids)
            meta['no_of_years']=no_of_years
            meta['resource_ids']=resource_ids
            if(len(no_of_years)!=0):
            	print('request_dividend_year=request_dividend_year&yearRange=' + str(year_to_be_processed) + '&resource_ids='+str(resource_ids))
            	yield self.make_request("http://www.cullenfunds.com/cullen-template/ajax-request-page.php",method=Statics.CRAWL_METHOD_POST,dont_filter=True ,callback=self.dividends, meta=meta, body='request_dividend_year=request_dividend_year&yearRange=' + str(year_to_be_processed) + '&resource_ids='+str(resource_ids), headers=headers)
        except Exception as e:
        	print(e)
        	traceback.print_exc()
        	for i in items:
        		i['capital_gains'] = list(itertools.chain.from_iterable(i['capital_gains']))
        		i['dividends'] = list(itertools.chain.from_iterable(i['dividends']))
        		yield self.generate_item(i, FinancialDetailItem)
