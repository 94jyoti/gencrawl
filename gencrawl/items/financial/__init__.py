from gencrawl.items import BaseItem
from scrapy import Field


class FinancialItem(BaseItem):
    fund_url = Field()
    instrument_name = Field()
    nasdaq_ticker = Field()
    cusip = Field()
    share_class = Field()
    job_id=Field()
    gencrawl_id=Field()

