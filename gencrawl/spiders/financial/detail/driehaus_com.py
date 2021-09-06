from gencrawl.spiders.financial.financial_detail_spider import FinancialDetailSpider
from gencrawl.spiders.financial.financial_detail_field_mapping import FinancialDetailFieldMapSpider
import scrapy


class DriehausComDetail(FinancialDetailFieldMapSpider):
    name = 'financial_detail_driehaus_com'

    def get_items_or_req(self, response, default_item=None):
        
        '''
        Since single url contains mulitple ticker so lenght of items is equivalent to 
        number of tickers available in that url.
        Also the multiple benchmark exists for each ticker in this parser.
        So First created a list of Benchmarks w.r.t. Ticker, then added each benchmark list
        with each ticker items and then created a seprated list i.e. total_items, that contains
        all created items along with benchmark and ticker.

        So sample output would be like :- url1 -- ticker1, benchmark1 and  benchmark 2
                                          url1 -- ticker2, benchmark1, benchmark 2, benchmark3
        '''
        
        total_items = []
        items = super().get_items_or_req(response, default_item)
        
        ticker_list = response.xpath(\
                        "//div['1'][@class='funds_info-container']//div[1]//dt[contains(text(),'Ticker')]/following-sibling::dd[1]/text()"\
                        ).extract()
        benchmark_text = response.xpath(\
                            "//h3[contains(text(),'Month-End Performance')]/following-sibling::div[2]//td[@class='data_table-data data_table-data--name']//text()"\
                            ).extract()
        
        benchmarks_dict = {}
        i = 0
        temp_list = []
        for item in benchmark_text:
            if item in ticker_list:
                i += 1
                temp_list = []
                continue
            else:
                temp_list.append(item)
            benchmarks_dict['list'+str(i)] = temp_list
        
        for j in range(len(items)):
            items[j]['nasdaq_ticker'] = response.xpath(\
                                        "//div['1'][@class='funds_info-container']//div[1]//dt[contains(text(),'Ticker')]/following-sibling::dd[1]/text()"\
                                        ).extract()[j]
            items[j]['minimum_additional_investment'] = response.xpath(\
                                                        "//dt[contains(text(),'Minimum Subsequent Investment')][1]/following-sibling::dd[1]/text()"\
                                                        ).extract()[j]
            key = 'list'+str(j+1)
            items[j]['benchmarks'] = benchmarks_dict[key]
            total_items.append(items[j])
        return total_items
