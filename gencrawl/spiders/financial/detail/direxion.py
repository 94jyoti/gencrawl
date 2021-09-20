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


class DirexionComDetail(FinancialDetailFieldMapSpider):
    name = 'financial_detail_direxion_com'
    allowed_domains = ["p6vg2dlkpverjbr2afvpbqupky.appsync-api.us-east-1.amazonaws.com"]

    def get_items_or_req(self, response, default_item={}):
        items = super().get_items_or_req(response, default_item)
        #items = self.prepare_mapped_items(response, default_item)
        file=open("hard.html","w")
        file.write(response.text)
        file.close()
        meta = response.meta
        meta['items'] = items
        url="https://p6vg2dlkpverjbr2afvpbqupky.appsync-api.us-east-1.amazonaws.com/graphql"
        body='{"operationName":"ListKurtosysFunds","variables":{"limit":300},"query":"query ListKurtosysFunds($filter: TableKurtosysFundsFilterInput, $limit: Int, $nextToken: String) {\n  listKurtosysFunds(filter: $filter, limit: $limit, nextToken: $nextToken) {\n    items {\n      Ticker\n      FundName\n      FundCode\n      Index\n      IndexName\n      Level1\n      Level2\n      Level3\n      Level4\n      Prospectus\n      Target\n      Duration\n      IntradayValue\n      IndexCusip\n      Distribution {\n        IncomeDividend\n        IncomeDividendConvertibleToReturnOfCapital\n        LongTermCapitalGain\n        ExDate\n        PayDate\n        RecordDate\n        ReturnOfCapital\n        ShortTermCapitalGain\n        APIInfo\n        __typename\n      }\n      Distributions {\n        IncomeDividend\n        IncomeDividendConvertibleToReturnOfCapital\n        LongTermCapitalGain\n        ExDate\n        PayDate\n        RecordDate\n        ReturnOfCapital\n        ShortTermCapitalGain\n        APIInfo\n        __typename\n      }\n      MonthlyMarketPerformance {\n        ExpenseRatioGross\n        ExpenseRatioNet\n        InceptionDate\n        TradeDate\n        ItemPerformanceType\n        OneMonth\n        ThreeMonth\n        YTD\n        OneYear\n        ThreeYear\n        FiveYear\n        TenYear\n        SinceInception\n        APIInfo\n        __typename\n      }\n      QuarterlyMarketPerformance {\n        ExpenseRatioGross\n        ExpenseRatioNet\n        InceptionDate\n        TradeDate\n        ItemPerformanceType\n        OneMonth\n        ThreeMonth\n        YTD\n        OneYear\n        ThreeYear\n        FiveYear\n        TenYear\n        SinceInception\n        APIInfo\n        __typename\n      }\n      MonthlyNavPerformance {\n        ExpenseRatioGross\n        ExpenseRatioNet\n        InceptionDate\n        TradeDate\n        ItemPerformanceType\n        OneMonth\n        ThreeMonth\n        YTD\n        OneYear\n        ThreeYear\n        FiveYear\n        TenYear\n        SinceInception\n        APIInfo\n        __typename\n      }\n      QuarterlyNavPerformance {\n        ExpenseRatioGross\n        ExpenseRatioNet\n        InceptionDate\n        TradeDate\n        ItemPerformanceType\n        OneMonth\n        ThreeMonth\n        YTD\n        OneYear\n        ThreeYear\n        FiveYear\n        TenYear\n        SinceInception\n        APIInfo\n        __typename\n      }\n      Pricing {\n        MarketClosingPrice\n        MarketClosingChangeDollar\n        MarketClosingChangePercent\n        Nav\n        NavChangeDollar\n        NavChangePercent\n        PremiumDiscount\n        Ticker\n        TradeDate\n        __typename\n      }\n      Url\n      TimeStamp\n      TradeDate\n      EndOfMonthDate\n      EndOfQuarterDate\n      EndOfQuarterHoldingsDate\n      EndOfQuarterBondStatisticsDate\n      EndOfQuarterPerformanceDate\n      APIInfo\n      __typename\n    }\n    nextToken\n    __typename\n  }\n}\n"}'
        #body='{"operationName":"ListKurtosysFunds","variables":{"limit":300},"query":"query ListKurtosysFunds($filter: TableKurtosysFundsFilterInput, $limit: Int, $nextToken: String) {\n  listKurtosysFunds(filter: $filter, limit: $limit, nextToken: $nextToken) {\n    items {\n      Ticker\n      FundName\n      FundCode\n      Index\n      IndexName\n      Level1\n      Level2\n      Level3\n      Level4\n      Prospectus\n      Target\n      Duration\n      IntradayValue\n      IndexCusip\n      Distribution {\n        IncomeDividend\n        IncomeDividendConvertibleToReturnOfCapital\n        LongTermCapitalGain\n        ExDate\n        PayDate\n        RecordDate\n        ReturnOfCapital\n        ShortTermCapitalGain\n        APIInfo\n        __typename\n      }\n      Distributions {\n        IncomeDividend\n        IncomeDividendConvertibleToReturnOfCapital\n        LongTermCapitalGain\n        ExDate\n        PayDate\n        RecordDate\n        ReturnOfCapital\n        ShortTermCapitalGain\n        APIInfo\n        __typename\n      }\n      MonthlyMarketPerformance {\n        ExpenseRatioGross\n        ExpenseRatioNet\n        InceptionDate\n        TradeDate\n        ItemPerformanceType\n        OneMonth\n        ThreeMonth\n        YTD\n        OneYear\n        ThreeYear\n        FiveYear\n        TenYear\n        SinceInception\n        APIInfo\n        __typename\n      }\n      QuarterlyMarketPerformance {\n        ExpenseRatioGross\n        ExpenseRatioNet\n        InceptionDate\n        TradeDate\n        ItemPerformanceType\n        OneMonth\n        ThreeMonth\n        YTD\n        OneYear\n        ThreeYear\n        FiveYear\n        TenYear\n        SinceInception\n        APIInfo\n        __typename\n      }\n      MonthlyNavPerformance {\n        ExpenseRatioGross\n        ExpenseRatioNet\n        InceptionDate\n        TradeDate\n        ItemPerformanceType\n        OneMonth\n        ThreeMonth\n        YTD\n        OneYear\n        ThreeYear\n        FiveYear\n        TenYear\n        SinceInception\n        APIInfo\n        __typename\n      }\n      QuarterlyNavPerformance {\n        ExpenseRatioGross\n        ExpenseRatioNet\n        InceptionDate\n        TradeDate\n        ItemPerformanceType\n        OneMonth\n        ThreeMonth\n        YTD\n        OneYear\n        ThreeYear\n        FiveYear\n        TenYear\n        SinceInception\n        APIInfo\n        __typename\n      }\n      Pricing {\n        MarketClosingPrice\n        MarketClosingChangeDollar\n        MarketClosingChangePercent\n        Nav\n        NavChangeDollar\n        NavChangePercent\n        PremiumDiscount\n        Ticker\n        TradeDate\n        __typename\n      }\n      Url\n      TimeStamp\n      TradeDate\n      EndOfMonthDate\n      EndOfQuarterDate\n      EndOfQuarterHoldingsDate\n      EndOfQuarterBondStatisticsDate\n      EndOfQuarterPerformanceDate\n      APIInfo\n      __typename\n    }\n    nextToken\n    __typename\n  }\n}\n"}'
        yield scrapy.Request(url,meta=meta,body=body,callback=self.dividends,method="Post",dont_filter=True)

    def dividends(self,response):
        items = response.meta['items']
        print("i am here")
        file = open("direxion_div.html", "w")
        file.write(response.text)
        file.close()
        print(response.text)


        #print(response.text)
        #return items
