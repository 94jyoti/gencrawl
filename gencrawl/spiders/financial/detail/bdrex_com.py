from gencrawl.spiders.financial.financial_detail_spider import FinancialDetailSpider
from gencrawl.spiders.financial.financial_detail_field_mapping import FinancialDetailFieldMapSpider
import scrapy
import re
from gencrawl.items.financial.financial_detail_item import FinancialDetailItem


class BdrexComDetail(FinancialDetailFieldMapSpider):
    name = 'financial_detail_bdrex_com'

    def get_items_or_req(self, response, default_item=None):
        items = super().get_items_or_req(response, default_item)
        gross_net_temp = (
        response.xpath("//div[@class='fund-section']//following::p[1]//small//text()").extract()[0]).split(",")
        for item in items:
            for i in gross_net_temp:
                if (item['share_class'] in i):
                    g_n = i.split("and")
                    for j in g_n:
                        if ("gross expenses" in j):
                            item['total_expense_gross'] = re.findall(r'\d*\.?\d+%', j)[0]
                        if ("reimbursement" in j):
                            item['total_expense_net'] = re.findall(r'\d*\.?\d+%', j)[0]

        manager_url = response.xpath("//a[contains(text(),'Portfolio Management & Advisers')]/@href").extract()[0]
        meta = response.meta
        meta['items'] = items
        yield self.make_request(manager_url, callback=self.fund_manager, meta=meta)

    def fund_manager(self, response):
        items = response.meta['items']
        fund_managers = response.xpath(
            "//h2[contains(text(),'Portfolio Managers')]/following::p//strong//text()").extract()
        fund_manager = []
        for i in fund_managers:
            d = {"fund_manager": ""}
            d["fund_manager"] = i
            fund_manager.append(d)
        advisors = response.xpath("//h2[contains(text(),'Adviser')]//text()").extract()[0]
        for item in items:
            item['fund_managers'] = fund_manager
            item['sub_advisor'] = advisors.replace("Adviser:", "").strip()
            yield self.generate_item(item, FinancialDetailItem)