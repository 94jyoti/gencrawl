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
from gencrawl.util.statics import Statics
# import urllib
import itertools
import traceback
import nltk
from nltk.corpus import wordnet


class AquilaComDetail(FinancialDetailFieldMapSpider):
    name = 'financial_detail_aquila_com'

    def get_items_or_req(self, response, default_item={}):
        items = super().get_items_or_req(response, default_item)
        print(len(items))
        file = open("aquila.html", "w")
        file.write(response.text)
        file.close()
        print("atyaxgausbasjcb")
        print(
            "//div[@id='home-slide-3']//table//tbody//td[contains(text(),'AZTFX')]/following-sibling::td[position()=last()]//text()")
        for item in items:
            temp_share_class = item['share_class'].lower()
            block_data = response.xpath(
                "//h3[contains(text(),'Fund Facts')]/parent::section//div[@class='" + temp_share_class + "']//ul//li")
            for data in block_data:
                if ("cusip" in data.xpath(".//text()").extract()[0].lower()):
                    item['cusip'] = data.xpath(".//span//text()").extract_first()
                if ("fund symbol" in data.xpath(".//text()").extract()[0].lower()):
                    item['nasdaq_ticker'] = data.xpath(".//span//text()").extract_first()
                if ("inception date" in data.xpath(".//text()").extract()[0].lower()):
                    item['share_inception_date'] = data.xpath(".//span//text()").extract_first()
                if ("total net assets" in data.xpath(".//text()").extract()[0].lower()):
                    item['portfolio_assets'] = data.xpath(".//span//text()").extract_first()+" "+re.findall(r'\(.*?\)',data.xpath(".//text()").extract()[0])[0].replace("(","").replace(")","")
                    print(item['portfolio_assets'])
                    item['portfolio_assets_date'] = data.xpath(".//text()").extract()[0].split("as of")[-1]
            # distributionss
            distribution_data = response.xpath("//div[contains(text(),'Distributions')]//@number").extract()[0]
            print(item['nasdaq_ticker'])
            try:
                item['sec_yield_30_day'] = response.xpath("//div[@id='home-slide-" + str(distribution_data) + "']//table//td[contains(text(),'" + item['nasdaq_ticker'] + "')]/following-sibling::td[position()=last()]//text()").extract()[0]
                item['sec_yield_date_30_day'] = (response.xpath("//div[@id='home-slide-" + str(distribution_data) + "']//span[contains(text(),'as of')][1]//text()").extract()[0]).replace("as of","").strip()
                item['distribution_yield_12_month'] = response.xpath("//div[@id='home-slide-" + str(distribution_data) + "']//table//td[contains(text(),'" + item['nasdaq_ticker'] + "')]/following-sibling::td[position()=2]//text()").extract()[0]
            except:
                pass

            # fees and expense
            expense_data = response.xpath("//div[contains(text(),'Fees & Expenses')]//@number").extract()[0]
            item['total_expense_gross'] = response.xpath("//div[@id='home-slide-" + str(expense_data) + "']//div[@class='" + item['share_class'].lower() + "']//table//th[contains(text(),'Total Operating Expense')]//following-sibling::td//text()").extract()[
                0]
            item['total_expense_net'] = response.xpath("//div[@id='home-slide-" + str(expense_data) + "']//div[@class='" + item['share_class'].lower() + "']//table//th[contains(text(),'Net Expense ratio')]//following-sibling::td//text()").extract()[0]
            print("feeebbbbb toal")
            try:
                item['fees_total_12b_1'] = response.xpath("//div[@id='home-slide-" + str(expense_data) + "']//div[@class='" + item['share_class'].lower() + "']//table//th[contains(text(),'12b-1')]//following-sibling::td//text()").extract()[0]
            except:
                pass
            print(item['fees_total_12b_1'] )
            # portflio managers
            print("manancbdjcbdh")
            managers_data = response.xpath("//div[contains(text(),'Portfolio Management')]//@number").extract()[0]
            manager_name = response.xpath("//div[@id='home-slide-5']//ul//li//p[1]//text()").extract()
            print("mananfefdedeeydudcgucgducducbdcdbcdcdbcd-----------",manager_name)
            fund_manager_list = []
            for name in manager_name:
                #print(name)
                person_list = []
                #person_names = person_list
                tokens = nltk.tokenize.word_tokenize(name)
                print(tokens)
                pos = nltk.pos_tag(tokens)
                sentt = nltk.ne_chunk(pos, binary=False)
                print("sennntnttntn",sentt)
                person = []
                name = ""

                for subtree in sentt.subtrees(filter=lambda t: t.label() == 'PERSON'):
                    print(subtree)
                    for leaf in subtree.leaves():
                        person.append(leaf[0])
                        print("knccnkdcnkdcndckdkckdc",person)
                    if len(person) >= 1:  # avoid grabbing lone surnames
                        for part in person:
                            name += part + ' '
                            print("nameeemeem",name)
                        if name[:-1] not in person_list:
                            print(person_list)
                            person_list.append(name[:-1])
                            print(person_list)
                        name = ''
                    person = []
                person_names = person_list
                print('personlist',person_list)
                for person in person_list:
                    person_split = person.split(" ")
                    for name in person_split:
                        if wordnet.synsets(name):
                            if (name in person):
                                person_names.remove(person)
                                break
                print(person_names)
                data_dict = {"fund_manager": ""}
                try:
                    data_dict['fund_manager'] = person_names[0]
                    fund_manager_list.append(data_dict)
                except:
                    pass
                print(fund_manager_list)
            item['fund_managers'] = fund_manager_list
            yield self.generate_item(item, FinancialDetailItem)
