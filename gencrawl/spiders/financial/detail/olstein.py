from gencrawl.spiders.financial.financial_detail_spider import FinancialDetailSpider
from gencrawl.spiders.financial.financial_detail_field_mapping import FinancialDetailFieldMapSpider
import scrapy
import re
from gencrawl.util.statics import Statics
import re
from gencrawl.items.financial.financial_detail_item import FinancialDetailItem


class OlsteinfundsComDetail(FinancialDetailFieldMapSpider):
    name = 'financial_detail_olstein_com'
    def get_items_or_req(self, response, default_item=None):
        items = super().get_items_or_req(response, default_item)
        file=open("olstin.html","w")
        file.write(response.text)
        file.close()

        url="https://www.olsteinfunds.com"+response.xpath("//h4[contains(text(),'"+items[0]['instrument_name']+"')][1]//following::li//a[contains(text(),'Performance')][1]//@href").extract()[0]
        meta = response.meta
        meta['items'] = items
        print(url)
        yield self.make_request(url, callback=self.parse_performance, meta=meta, dont_filter=True, method=Statics.CRAWL_METHOD_SELENIUM)

    def parse_performance(self,response):
        print("cdcw")

        items = response.meta['items']
        for item in items:
            temp=item['share_class'].lower().replace("class","").strip()
            temp_instrument_name="-".join(item['instrument_name'].lower().split(" "))
            print(temp)
            print(temp_instrument_name)


            if(temp=="advisor"):
                temp="adviser"

            if(len(response.xpath("(//div[contains(@id,'"+temp_instrument_name+"-class-"+temp+"')]//table)[1]//thead//th//text()").extract())==0):
                benchmark_temp = response.xpath(
                    "(//div[contains(@id,'"+temp_instrument_name+"-"+temp + "-class')]//table)[1]//thead//th"
                                                                     ""
                                                                     " | (//div[@id='class-"+temp+"-performance']//table)[1]//thead//th")
            #benchmark_temp=[''.join(x) for x in zip(benchmark_temp[0::2], benchmark_temp[1::2])]
            print(benchmark_temp)
            print("--------------------------------------------")
            benchmark_list=[]
            for row in benchmark_temp:
                print(row)
                td_text=row.xpath(".//text()").extract()
                print(td_text)
                benchmarks=" ".join(td_text)
                print("bnnennenenenenenenenn",benchmarks)
                if("Index" in benchmarks):
                        benchmark_list.append(benchmarks)
                item['benchmarks']=benchmark_list
                print("finanannanananna",item['benchmarks'])
            yield self.generate_item(item, FinancialDetailItem)
