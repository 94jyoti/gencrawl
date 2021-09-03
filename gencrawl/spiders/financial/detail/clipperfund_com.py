from gencrawl.spiders.financial.financial_detail_spider import FinancialDetailSpider
from gencrawl.spiders.financial.financial_detail_field_mapping import FinancialDetailFieldMapSpider
import scrapy


class ClipperfundComDetail(FinancialDetailFieldMapSpider):
    name = 'financial_detail_clipperfund_com'

    def get_items_or_req(self, response, default_item=None):
        items = super().get_items_or_req(response, default_item)
        home_page_url = response.xpath("//a[contains(text(),'Home')]/@href").extract()[0]
        meta = response.meta
        meta['items'] = items
        resp = self.make_request(home_page_url, callback=self.parse_ticker_cusip, meta=meta)
        return resp


    def parse_ticker_cusip(self, response):
        # Extracting ticker and cusip from home page
        items = response.meta['items']
        items[0]['nasdaq_ticker'] = response.xpath(\
            "//tr[th[contains(text(),'Ticker')]]/following-sibling::tr/td[4]/text()"\
                                                                        ).extract()[0]

        items[0]['cusip'] = response.xpath(\
            "//tr[th[contains(text(),'CUSIP')]]/following-sibling::tr/td[6]/text()"\
                                                                        ).extract()[0]
        return items