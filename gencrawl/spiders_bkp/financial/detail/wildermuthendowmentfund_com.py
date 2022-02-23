from gencrawl.spiders.financial.financial_detail_spider import FinancialDetailSpider
from gencrawl.spiders.financial.financial_detail_field_mapping import FinancialDetailFieldMapSpider
from gencrawl.items.financial.financial_detail_item import FinancialDetailItem
import scrapy


class WilderDetail(FinancialDetailFieldMapSpider):
    name = 'financial_detail_wilder_com'

    def get_items_or_req(self, response, default_item={}):
        items = super().get_items_or_req(response, default_item)
        about_us_url = response.xpath("//span[contains(text(),'About Us')]/parent::a/@href").extract()[0]
        meta = response.meta
        meta['items'] = items
        yield self.make_request(about_us_url, callback=self.fund_manager, meta=meta)

    def fund_manager(self, response):
        items = response.meta['items']
        fund_manager_temp = response.xpath(
            "//h3[contains(text(),'Founder and Portfolio Manager')]/parent::div/h4/text()[1]").extract()
        sub_advisor = response.xpath(
            "//h3[contains(text(),'Founder and Portfolio Manager')]/parent::div//following-sibling::a/strong//text()").extract()
        fund_manager_list = []
        for manager in fund_manager_temp:
            dict = {"fund_manager": ""}
            dict['fund_manager'] = manager.replace(",","")
            fund_manager_list.append(dict)

        for item in items:
            item['fund_managers'] = fund_manager_list
            item['sub_advisor'] = sub_advisor

        meta = response.meta
        meta['items'] = items
        investment_url = response.xpath("//span[contains(text(),'Investment Strategy')]/parent::a/@href").extract()[0]
        yield self.make_request(investment_url, callback=self.investment_strategy, meta=meta)

    def investment_strategy(self, response):
        items = response.meta['items']
        investment_objective = response.xpath(
            "//h3[contains(text(),'Investment Objective')]/following::p[1]/text()").extract()[0]
        investment_strategy = " ".join(response.xpath(
            "//h3[contains(text(),'Investment Strategy')]/parent::div/p/text()").extract())
        for item in items:
            item['investment_objective'] = investment_objective
            item['investment_strategy'] = investment_strategy
            yield self.generate_item(item, FinancialDetailItem)

