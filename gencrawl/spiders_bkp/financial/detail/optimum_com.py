from gencrawl.spiders.financial.financial_detail_spider import FinancialDetailSpider
from gencrawl.util.statics import Statics
import json
import scrapy
from gencrawl.items.financial.financial_detail_item import FinancialDetailItem
from datetime import datetime
import datetime
import urllib.parse
from gencrawl.util.statics import Statics

import re


class OptimumComDetail(FinancialDetailSpider):
    name = 'financial_detail_optimum_com'
    custom_settings = {
        "RETRY_TIMES": 5,
        "CRAWLERA_ENABLED": False,
        "DOWNLOAD_DELAY": 4
    }

    def get_items_or_req(self, response, default_item={}):
        items = self.prepare_items(response, default_item)
        for item in items:
            fund_manager_list = []
            if (response.xpath(
                    "//h4[contains(text(),'Investment') or contains(text(),'Director')]/preceding-sibling::h3[1]").extract()):
                fund_manager = response.xpath(
                    "//h4[contains(text(),'Investment') or contains(text(),'Director')]/preceding-sibling::h3[1]").extract()
                start_date_fund = response.xpath("//p[contains(text(),'Start date')]//text()").extract()
                for i in range(len(fund_manager)):
                    data_dict = {"fund_manager": "", "fund_manager_years_of_experience_with_fund": ""}
                    data_dict['fund_manager'] = fund_manager[i]
                    data_dict['fund_manager_years_of_experience_with_fund'] = start_date_fund[i].split(":")[-1]
                    fund_manager_list.append(data_dict)
            elif (response.xpath(
                    "//p[contains(text(),'Start date on the Fund')]//preceding-sibling::h3//text() | //h5[contains(text(),'Manager')]//preceding-sibling::h4//text()").extract()):
                fund_manager = response.xpath("//p[contains(text(),'Start date on the Fund')]//preceding-sibling::h3//text() | //h5[contains(text(),'Manager')]//preceding-sibling::h4//text()").extract()
                start_date_fund = response.xpath("//*[contains(text(),'Start date on the Fund')]//text()").extract()
                for i in range(len(fund_manager)):
                    data_dict = {"fund_manager": "", "fund_manager_years_of_experience_with_fund": ""}
                    data_dict['fund_manager'] = fund_manager[i]
                    data_dict['fund_manager_years_of_experience_with_fund'] = start_date_fund[i].split(":")[-1]
                    fund_manager_list.append(data_dict)
            else:
                fund_manager=response.xpath("//h4[contains(text(),'Investment') or contains(text(),'Portfolio')]//preceding-sibling::h3[1]//text()").extract()
                start_date_fund = response.xpath("//h4[contains(text(),'Portfolio')]/following-sibling::p[1][contains(text(),'Start date on the Fund')]//text()").extract()
                for i in range(len(fund_manager)):
                    data_dict = {"fund_manager": "", "fund_manager_years_of_experience_with_fund": ""}
                    data_dict['fund_manager'] = fund_manager[i]
                    data_dict['fund_manager_years_of_experience_with_fund'] = start_date_fund[i].split(":")[-1]
                    fund_manager_list.append(data_dict)

            item['fund_managers'] = fund_manager_list
            yield self.generate_item(item, FinancialDetailItem)