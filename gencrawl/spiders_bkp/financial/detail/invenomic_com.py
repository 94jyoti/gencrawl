from gencrawl.spiders.financial.financial_detail_spider import FinancialDetailSpider
from gencrawl.spiders.financial.financial_detail_field_mapping import FinancialDetailFieldMapSpider
import scrapy
import re
from gencrawl.util.statics import Statics
import re
from gencrawl.items.financial.financial_detail_item import FinancialDetailItem
import json
from copy import deepcopy

class InvenomicDetail(FinancialDetailFieldMapSpider):
    name = 'financial_detail_invenomic_com'

    def get_items_or_req(self, response, default_item=None):
        temp_items = super().get_items_or_req(response, default_item)
        url=response.xpath("(//iframe[@title='Table Master'])[position()=last()]//@src").extract()[0]
        temp_url=response.xpath("(//span[contains(text(),'Quarter')]//following::iframe)[position()=1]//@src").extract()[0]
        meta = response.meta
        meta['temp_items'] = temp_items
        meta['temp_url']=temp_url
        yield self.make_request(url, callback=self.parse_sharetable, meta=meta, dont_filter=True,method=Statics.CRAWL_METHOD_SELENIUM)

    def parse_sharetable(self, response):
        temp_items = response.meta['temp_items']
        temp_url=response.meta['temp_url']
        data=re.findall("<script .*?>.*?var initialState = ({.*?});.*?</script>",response.text.replace("\n",""))[0]
        json_data=((json.loads(data))['data']['settings']['data']['csvString']).split("\n")
        for data in range(len(json_data)):
            if("Ticker" in json_data[data]):
                temp_ticker = json_data[data].split(",")[1:]
            if("Share Class" in json_data[data]):
                temp_share_class=json_data[data].split(",")[1:]
            if("Investment" in json_data[data]):
                s = re.compile(r'"[^"]*"|[^,]+')
                temp_min_investment=s.findall(json_data[data])[1:]
            if("Management Fee" in json_data[data]):
                temp_fee=json_data[data].split(",")[1:]
            if ("Gross" in json_data[data]):
                temp_gross = json_data[data].split(",")[1:]
            if ("Net" in json_data[data]):
                temp_net = json_data[data].split(",")[1:]
        items=[]
        for count in range(len(temp_ticker)):
            temp_items[0]['nasdaq_ticker']=temp_ticker[count]
            temp_items[0]['share_class'] = temp_share_class[count]
            temp_items[0]['minimum_initial_investment'] = temp_min_investment[count].replace("'","").replace('"','')
            temp_items[0]['management_fee'] = temp_fee[count]
            temp_items[0]['total_expense_gross'] = temp_gross[count]
            temp_items[0]['total_expense_net'] = temp_net[count]
            items.append(deepcopy(temp_items[0]))
        meta = response.meta
        meta['items'] = items
        yield self.make_request(temp_url, callback=self.parse_benchmarks, meta=meta, dont_filter=True,method=Statics.CRAWL_METHOD_SELENIUM)

    def parse_benchmarks(self, response):
        items = response.meta['items']
        data=re.findall("<script .*?>.*?var initialState = ({.*?});.*?</script>",response.text.replace("\n",""))[0]
        json_data = ((json.loads(data))['data']['settings']['data']['csvString']).split("\n")
        benchmark_list=[]
        for i in json_data:
            temp = i.split(",")
            for benchmark in temp:
                if ("Index" in benchmark):
                    benchmark_list.append(benchmark)
        for item in items:
            item['benchmarks']=benchmark_list
            yield self.generate_item(item, FinancialDetailItem)


