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
from datetime import date, datetime
# import date_converter



class DirexionComDetail(FinancialDetailFieldMapSpider):
    name = 'financial_detail_direxion_com'
    allowed_domains = ["p6vg2dlkpverjbr2afvpbqupky.appsync-api.us-east-1.amazonaws.com"]
    custom_settings = {
        "HTTPCACHE_ENABLED": False,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 2,
        "DOWNLOAD_DELAY": 4,
        "COOKIES_ENABLED": True,
        "COOKIES_DEBUG": True,
        "CRAWLERA_ENABLED": True
    }

    def get_items_or_req(self, response, default_item={}):
        items = super().get_items_or_req(response, default_item)
        #items = self.prepare_mapped_items(response, default_item)
        file=open("hard.html","w")
        file.write(response.text)
        file.close()
        meta = response.meta
        meta['items'] = items
        url="https://p6vg2dlkpverjbr2afvpbqupky.appsync-api.us-east-1.amazonaws.com/graphql"
        #body='{"operationName":"ListKurtosysFunds","variables":{"limit":300},"query":"query ListKurtosysFunds($filter: TableKurtosysFundsFilterInput, $limit: Int, $nextToken: String) {\n  listKurtosysFunds(filter: $filter, limit: $limit, nextToken: $nextToken) {\n    items {\n      Ticker\n      FundName\n      FundCode\n      Index\n      IndexName\n      Level1\n      Level2\n      Level3\n      Level4\n      Prospectus\n      Target\n      Duration\n      IntradayValue\n      IndexCusip\n      Distribution {\n        IncomeDividend\n        IncomeDividendConvertibleToReturnOfCapital\n        LongTermCapitalGain\n        ExDate\n        PayDate\n        RecordDate\n        ReturnOfCapital\n        ShortTermCapitalGain\n        APIInfo\n        __typename\n      }\n      Distributions {\n        IncomeDividend\n        IncomeDividendConvertibleToReturnOfCapital\n        LongTermCapitalGain\n        ExDate\n        PayDate\n        RecordDate\n        ReturnOfCapital\n        ShortTermCapitalGain\n        APIInfo\n        __typename\n      }\n      MonthlyMarketPerformance {\n        ExpenseRatioGross\n        ExpenseRatioNet\n        InceptionDate\n        TradeDate\n        ItemPerformanceType\n        OneMonth\n        ThreeMonth\n        YTD\n        OneYear\n        ThreeYear\n        FiveYear\n        TenYear\n        SinceInception\n        APIInfo\n        __typename\n      }\n      QuarterlyMarketPerformance {\n        ExpenseRatioGross\n        ExpenseRatioNet\n        InceptionDate\n        TradeDate\n        ItemPerformanceType\n        OneMonth\n        ThreeMonth\n        YTD\n        OneYear\n        ThreeYear\n        FiveYear\n        TenYear\n        SinceInception\n        APIInfo\n        __typename\n      }\n      MonthlyNavPerformance {\n        ExpenseRatioGross\n        ExpenseRatioNet\n        InceptionDate\n        TradeDate\n        ItemPerformanceType\n        OneMonth\n        ThreeMonth\n        YTD\n        OneYear\n        ThreeYear\n        FiveYear\n        TenYear\n        SinceInception\n        APIInfo\n        __typename\n      }\n      QuarterlyNavPerformance {\n        ExpenseRatioGross\n        ExpenseRatioNet\n        InceptionDate\n        TradeDate\n        ItemPerformanceType\n        OneMonth\n        ThreeMonth\n        YTD\n        OneYear\n        ThreeYear\n        FiveYear\n        TenYear\n        SinceInception\n        APIInfo\n        __typename\n      }\n      Pricing {\n        MarketClosingPrice\n        MarketClosingChangeDollar\n        MarketClosingChangePercent\n        Nav\n        NavChangeDollar\n        NavChangePercent\n        PremiumDiscount\n        Ticker\n        TradeDate\n        __typename\n      }\n      Url\n      TimeStamp\n      TradeDate\n      EndOfMonthDate\n      EndOfQuarterDate\n      EndOfQuarterHoldingsDate\n      EndOfQuarterBondStatisticsDate\n      EndOfQuarterPerformanceDate\n      APIInfo\n      __typename\n    }\n    nextToken\n    __typename\n  }\n}\n"}'
        #payload={'operationName': "ListKurtosysFunds", 'variables': ''{limit: 300}'},'operationName': "ListKurtosysFunds",'query':' "query ListKurtosysFunds($filter: TableKurtosysFundsFilterInput, $limit: Int, $nextToken: String) {\n  listKurtosysFunds(filter: $filter, limit: $limit, nextToken: $nextToken) {\n    items {\n      Ticker\n      FundName\n      FundCode\n      Index\n      IndexName\n      Level1\n      Level2\n      Level3\n      Level4\n      Prospectus\n      Target\n      Duration\n      IntradayValue\n      IndexCusip\n      Distribution {\n        IncomeDividend\n        IncomeDividendConvertibleToReturnOfCapital\n        LongTermCapitalGain\n        ExDate\n        PayDate\n        RecordDate\n        ReturnOfCapital\n        ShortTermCapitalGain\n        APIInfo\n        __typename\n      }\n      Distributions {\n        IncomeDividend\n        IncomeDividendConvertibleToReturnOfCapital\n        LongTermCapitalGain\n        ExDate\n        PayDate\n        RecordDate\n        ReturnOfCapital\n        ShortTermCapitalGain\n        APIInfo\n        __typename\n      }\n      MonthlyMarketPerformance {\n        ExpenseRatioGross\n        ExpenseRatioNet\n        InceptionDate\n        TradeDate\n        ItemPerformanceType\n        OneMonth\n        ThreeMonth\n        YTD\n        OneYear\n        ThreeYear\n        FiveYear\n        TenYear\n        SinceInception\n        APIInfo\n        __typename\n      }\n      QuarterlyMarketPerformance {\n        ExpenseRatioGross\n        ExpenseRatioNet\n        InceptionDate\n        TradeDate\n        ItemPerformanceType\n        OneMonth\n        ThreeMonth\n        YTD\n        OneYear\n        ThreeYear\n        FiveYear\n        TenYear\n        SinceInception\n        APIInfo\n        __typename\n      }\n      MonthlyNavPerformance {\n        ExpenseRatioGross\n        ExpenseRatioNet\n        InceptionDate\n        TradeDate\n        ItemPerformanceType\n        OneMonth\n        ThreeMonth\n        YTD\n        OneYear\n        ThreeYear\n        FiveYear\n        TenYear\n        SinceInception\n        APIInfo\n        __typename\n      }\n      QuarterlyNavPerformance {\n        ExpenseRatioGross\n        ExpenseRatioNet\n        InceptionDate\n        TradeDate\n        ItemPerformanceType\n        OneMonth\n        ThreeMonth\n        YTD\n        OneYear\n        ThreeYear\n        FiveYear\n        TenYear\n        SinceInception\n        APIInfo\n        __typename\n      }\n      Pricing {\n        MarketClosingPrice\n        MarketClosingChangeDollar\n        MarketClosingChangePercent\n        Nav\n        NavChangeDollar\n        NavChangePercent\n        PremiumDiscount\n        Ticker\n        TradeDate\n        __typename\n      }\n      Url\n      TimeStamp\n      TradeDate\n      EndOfMonthDate\n      EndOfQuarterDate\n      EndOfQuarterHoldingsDate\n      EndOfQuarterBondStatisticsDate\n      EndOfQuarterPerformanceDate\n      APIInfo\n      __typename\n    }\n    nextToken\n    __typename\n  }\n}\n"','variables': '{'limit': '300'}'}
        body={"operationName":"ListKurtosysFunds","variables":{"limit":300},"query":"query ListKurtosysFunds($filter: TableKurtosysFundsFilterInput, $limit: Int, $nextToken: String) {\n  listKurtosysFunds(filter: $filter, limit: $limit, nextToken: $nextToken) {\n    items {\n      Ticker\n      FundName\n      FundCode\n      Index\n      IndexName\n      Level1\n      Level2\n      Level3\n      Level4\n      Prospectus\n      Target\n      Duration\n      IntradayValue\n      IndexCusip\n      Distribution {\n        IncomeDividend\n        IncomeDividendConvertibleToReturnOfCapital\n        LongTermCapitalGain\n        ExDate\n        PayDate\n        RecordDate\n        ReturnOfCapital\n        ShortTermCapitalGain\n        APIInfo\n        __typename\n      }\n      Distributions {\n        IncomeDividend\n        IncomeDividendConvertibleToReturnOfCapital\n        LongTermCapitalGain\n        ExDate\n        PayDate\n        RecordDate\n        ReturnOfCapital\n        ShortTermCapitalGain\n        APIInfo\n        __typename\n      }\n      MonthlyMarketPerformance {\n        ExpenseRatioGross\n        ExpenseRatioNet\n        InceptionDate\n        TradeDate\n        ItemPerformanceType\n        OneMonth\n        ThreeMonth\n        YTD\n        OneYear\n        ThreeYear\n        FiveYear\n        TenYear\n        SinceInception\n        APIInfo\n        __typename\n      }\n      QuarterlyMarketPerformance {\n        ExpenseRatioGross\n        ExpenseRatioNet\n        InceptionDate\n        TradeDate\n        ItemPerformanceType\n        OneMonth\n        ThreeMonth\n        YTD\n        OneYear\n        ThreeYear\n        FiveYear\n        TenYear\n        SinceInception\n        APIInfo\n        __typename\n      }\n      MonthlyNavPerformance {\n        ExpenseRatioGross\n        ExpenseRatioNet\n        InceptionDate\n        TradeDate\n        ItemPerformanceType\n        OneMonth\n        ThreeMonth\n        YTD\n        OneYear\n        ThreeYear\n        FiveYear\n        TenYear\n        SinceInception\n        APIInfo\n        __typename\n      }\n      QuarterlyNavPerformance {\n        ExpenseRatioGross\n        ExpenseRatioNet\n        InceptionDate\n        TradeDate\n        ItemPerformanceType\n        OneMonth\n        ThreeMonth\n        YTD\n        OneYear\n        ThreeYear\n        FiveYear\n        TenYear\n        SinceInception\n        APIInfo\n        __typename\n      }\n      Pricing {\n        MarketClosingPrice\n        MarketClosingChangeDollar\n        MarketClosingChangePercent\n        Nav\n        NavChangeDollar\n        NavChangePercent\n        PremiumDiscount\n        Ticker\n        TradeDate\n        __typename\n      }\n      Url\n      TimeStamp\n      TradeDate\n      EndOfMonthDate\n      EndOfQuarterDate\n      EndOfQuarterHoldingsDate\n      EndOfQuarterBondStatisticsDate\n      EndOfQuarterPerformanceDate\n      APIInfo\n      __typename\n    }\n    nextToken\n    __typename\n  }\n}\n"}
        headers={"authority": "p6vg2dlkpverjbr2afvpbqupky.appsync-api.us-east-1.amazonaws.com","method": "POST","path": "/graphql","scheme": "https","accept": "*/*","accept-encoding": "gzip, deflate, br","accept-language": "en-GB,en-US;q=0.9,en;q=0.8","content-type": "application/json","origin": "https://www.direxion.com","referer": "https://www.direxion.com/","sec-ch-ua": '"Google Chrome";v="93", " Not;A Brand";v="99", "Chromium";v="93"',"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36","x-amz-user-agent": "aws-amplify/2.0.3","x-api-key": "da2-iafcow2bfbcgfj7l2yk4rixypm"}
        yield scrapy.Request(url,headers=headers,meta=meta,body=json.dumps(body),callback=self.dividends,method="POST",dont_filter=True)

    def dividends(self,response):
        items = response.meta['items']
        print("i am here")
        file = open("direxion_div.html", "w")
        file.write(response.text)
        file.close()
        json_data=json.loads(response.text)

        for row in json_data['data']['listKurtosysFunds']['items']:
            capital_gain_list=[]
            dividend_list=[]
            for item in items:
                if(row['Ticker'] in item['nasdaq_ticker']):
                    for data in row['Distributions']:
                        data_dict1 = {"ex_date": "", "pay_date": "", "ordinary_income": "", "qualified_income": "","record_date": "", "per_share": "", "reinvestment_price": ""}
                        data_dict2 = {'long_term_per_share': "", 'cg_ex_date': "", 'cg_record_date': "", 'cg_pay_date': "",'short_term_per_share': "", 'total_per_share': "", 'cg_reinvestment_price': ""}
                        temp_ex_date = data['ExDate']
                        # data_dict1['ex_date']=date_converter.string_to_string(temp_ex_date, '%m%d%Y', '%m-%d-%Y')
                        data_dict1['ex_date']=''
                        pay_date_temp = data['PayDate']
                        # data_dict1['pay_date']=date_converter.string_to_string(pay_date_temp, '%m%d%Y', '%m-%d-%Y')
                        data_dict1['pay_date']=''
                        temp_record_date= data['RecordDate']
                        # data_dict1['record_date'] =date_converter.string_to_string(temp_record_date, '%m%d%Y', '%m-%d-%Y')
                        data_dict1['record_date']=''
                        data_dict2['short_term_per_share'] = data['ShortTermCapitalGain']
                        data_dict2['long_term_per_share'] = data['LongTermCapitalGain']
                        data_dict1['ordinary_income'] = data['IncomeDividend']
                        capital_gain_list.append(data_dict2)
                        dividend_list.append(data_dict1)
                    item['capital_gains'] = capital_gain_list
                    item['dividends'] = dividend_list
                    yield self.generate_item(item, FinancialDetailItem)

        #print(response.text)
        #return items
