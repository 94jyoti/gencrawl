from gencrawl.spiders.financial.financial_detail_spider import FinancialDetailSpider
from gencrawl.spiders.financial.financial_detail_field_mapping import FinancialDetailFieldMapSpider
import scrapy
import re


class BrookefieldfundsComDetail(FinancialDetailFieldMapSpider):
    name = 'financial_detail_brookefield_com'
    custom_settings = {
        "RETRY_TIMES": 5,
        "CRAWLERA_ENABLED": True
    }
    def get_items_or_req(self, response, default_item=None):
        items = super().get_items_or_req(response, default_item)
        file=open("brroke_test.html","w")
        file.write(response.text)
        file.close()
        for item in items:
            item['share_inception_date']=response.xpath("//div[contains(@class,'key-stats-container key')]//p[contains(@class,'stat-value InceptionDate')]//span[contains(@class,'"+item['nasdaq_ticker']+"')]//text()").extract()[0]
            item['sec_yield_30_day']=response.xpath("//div[contains(@class,'key-stats-container key')]//p[contains(@class,'ThirtyDaySECYieldSubsidized')]//span[contains(@class,'"+item['nasdaq_ticker']+"')]//text()").extract()[0]
            item['portfolio_assets']=response.xpath("//div[contains(@class,'key-stats-container key')]//p[contains(@class,'TotalNetAssets')]//span[contains(@class,'"+item['nasdaq_ticker']+"')]//text()").extract()[0]
            item['distribution_frequency']=response.xpath("//div[contains(@class,'key-stats-container key')]//p[contains(@class,'DistributionFrequency')]//span[contains(@class,'"+item['nasdaq_ticker']+"')]//text()").extract()[0]
            item['sec_yield_without_waivers_30_day']=response.xpath("//div[contains(@class,'key-stats-container key')]//p[contains(@class,'ThirtyDaySECYieldUnsubsidized')]//span[contains(@class,'"+item['nasdaq_ticker']+"')]//text()").extract()[0]
            try:
                item['total_net_assets']=response.xpath("//td[contains(text(),'Net assets')]//following-sibling::td//text()").extract()[0]+" "+response.xpath("//td[contains(text(),'Net assets')]//text()").extract()[0].split("(")[-1].replace(")","")
            except:
                item['total_net_assets'] = \
                response.xpath("//td[contains(text(),'Net Assets')]//following-sibling::td//text()").extract()[
                    0] + " " + response.xpath("//td[contains(text(),'Net Assets')]//text()").extract()[0].split("(")[
                    -1].replace(")", "")
            try:
                item['total_net_assets_date']=response.xpath("//p[contains(text(),'as of')]//text()").extract()[0].replace("as of","").replace("(","").replace(")","")
            except:
                pass
            benchmark=response.xpath("//p[contains(text(),'Class/Benchmark')]/following::text()[1][contains(.,'Index')]").extract()
            item['benchmarks']=list(set(benchmark))

            item['nasdaq_ticker']=''.join(i for i in item['nasdaq_ticker'] if not i.isdigit())
            try:
                gross_net=response.xpath("//p[contains(text(),'gross')]//text()").extract()[0].split("Class")
            except:
                gross_net=response.xpath("//strong[contains(text(),'gross')]//text()").extract()[0].split(";")[-1].split("Class")
            try:
                for iter in gross_net:
                        data=iter.split("and")
                        print(data)
                        print(iter in item['share_class'])
                        if(item['share_class'].replace("Class","") in iter):
                            print(iter)
                            for i in data:
                                print("isnide fri")
                                if("gross" in i):
                                    print("yes")
                                    item['total_expense_gross']=re.findall(r'\d*\.?\d+', i)[0]
                                    print(item['total_expense_gross'])
                                if("net" in i):
                                    print("yes donee")
                                    item['total_expense_net']=re.findall(r'\d*\.?\d+', i)[0]
                #print(gross_net)
            except:
                pass

        return items

