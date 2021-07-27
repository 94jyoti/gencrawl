from gencrawl.spiders.financial.financial_detail_spider import FinancialDetailSpider
from gencrawl.spiders.financial.financial_detail_field_mapping import FinancialDetailFieldMapSpider
from gencrawl.items.financial.financial_detail_item import FinancialDetailItem
import scrapy
from dateutil.parser import parse

class GreencenturyComDetail(FinancialDetailSpider):
    name = 'financial_detail_greencentury_com'

    def get_items_or_req(self, response, default_item=None):
        parsed_items = []
        items = self.prepare_items(response, default_item)
        
        inception_date = response.xpath('//strong[contains(text(),"Inception Date")]/following-sibling::text()[1]').extract_first().strip()
        try:
            parse(str(inception_date), fuzzy=True)
            share_inception_date = inception_date
        except:
            share_inception_date = response.xpath('//strong[contains(text(),"Inception Date")]/following-sibling::text()[2]').extract_first().strip()

        body = response.xpath('//strong[contains(text(),"Expense Ratio")]/parent::span/parent::p//text()').extract()
        leng = len(body)
        len1 = None
        len2 = None
        len3 = None
        len4 = None
        for i in range(leng):
            if 'Expense Ratio' in body[i]:
                for j in range(i,leng):
                    if body[j].strip() != '' and 'Individual' in body[j].strip():
                        len1 = j
                        break
                for k in range(len1,leng):
                    if body[k].strip() != '' and 'Institutional' in body[k].strip():
                        len2 = k
                        break
            elif 'Minimum Investment/Fund' in body[i]:
                for j in range(i,leng):
                    if body[j].strip() != '' and 'Regular' in body[j].strip():
                        len3 = j
                        break
                for k in range(len3,leng):
                    if body[k].strip() != '' and 'Institutional' in body[k].strip():
                        len4 = k
                        break
        for item in items:
            if 'Individual' in item['share_class'] or 'Investor' in item['share_class']:
                item['total_expense_gross'] = body[len1].split(':')[1].strip()
                item['minimum_initial_investment'] = body[len3].split(':')[1].strip()
            elif 'Institutional' in item['share_class']:
                item['total_expense_gross'] = body[len2].split(':')[1].strip()
                item['minimum_initial_investment'] = body[len4].split(':')[1].strip()

            item['share_inception_date'] = share_inception_date
            item['investment_objective'] = ' '.join(response.xpath('//h3[contains(text(),"Objective")]/following-sibling::p[count(preceding-sibling::h3)=1]/descendant-or-self::text()').extract()).strip()
            item['investment_strategy'] = ' '.join(response.xpath('//h3[contains(text(),"Investment Strategy")]/following-sibling::p[count(preceding-sibling::h3)=2]/descendant-or-self::text()').extract()).strip()
            item['fund_managers'] = response.xpath('//img[contains(@class,"wp-image-") and contains(@src,"data:image") and not(contains(@class,"fl-photo"))]/parent::p/parent::div/h4/text()').extract()
            item['fees_total_12b_1'] = response.xpath("//strong[contains(text(),'Sales Charge')]/parent::span/text()[contains(.,'12b-1 Fee')]").get().split(':')[1]
            item['deferred_sales_charge'] = response.xpath("//strong[contains(text(),'Sales Charge')]/parent::span/text()[contains(.,'Back End Load')]").get().split(':')[1]
            item['redemption_fee'] = response.xpath("//strong[contains(text(),'Redemption Fee')]/following-sibling::text()[1]").get().split('(')[0]
            item['maximum_sales_charge_full_load'] = response.xpath("//strong[contains(text(),'Sales Charge')]/parent::span/text()[contains(.,'Front End Load')]").get().split(':')[1]
            item['sub_advisor'] = response.xpath("//span[contains(text(),'Investment Sub-advisor')]/text()").get().split(':')[1]
            parsed_items.append(self.generate_item(item, FinancialDetailItem))
        return parsed_items
