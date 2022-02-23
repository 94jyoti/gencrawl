from gencrawl.spiders.financial.financial_detail_spider import FinancialDetailSpider
from gencrawl.spiders.financial.financial_detail_field_mapping import FinancialDetailFieldMapSpider
import scrapy


class JamesinvestmentComDetail(FinancialDetailFieldMapSpider):
    name = 'financial_detail_jamesinvestment_com'

    def get_items_or_req(self, response, default_item=None):
        items = super().get_items_or_req(response, default_item)
        # 
        total_items = []
        complete_distribution = response.xpath("//tr[contains(@class,'fundInfo')]")
        
        total_tickers = len(items)
        for j in range(len(items)):
            dividends = []
            capital_gains = []
            for row in complete_distribution:
                divident_dict = {}
                capital_gains_dict = {}
                ex_date = row.xpath('./td[1]/text()').extract()[0]
                pay_date = row.xpath('./td[2]/text()').extract()[0]

                if total_tickers > 1:
                    if j == 0:
                        per_share = row.xpath('./td[4]/text()').extract()[0]
                        reinvestment_price = row.xpath('./td[5]/text()').extract()[0]
                    else:
                        per_share = row.xpath('./td[6]/text()').extract()[0]
                        reinvestment_price = row.xpath('./td[7]/text()').extract()[0]
                    divident_type = row.xpath('./td[3]/text()').extract()[0]
                else:
                    per_share = row.xpath('./td[5]/text()').extract()[0]
                    reinvestment_price = row.xpath('./td[3]/text()').extract()[0]
                    divident_type = row.xpath('./td[4]/text()').extract()[0]

                if divident_type == 'Income':
                    divident_dict = {'ex_date':ex_date, 'pay_date':pay_date,\
                                'per_share':per_share,\
                                'reinvestment_price':reinvestment_price}
                    dividends.append(divident_dict)
                else:
                    # divident_dict = {'ex_date':'', 'pay_date':'',\
                    #             'per_share':'',\
                    #             'reinvestment_price':''}
                    
                    if divident_type == 'Long Term Cap Gain':
                        capital_gains_dict = {'cg_ex_date':ex_date, 'cg_pay_date':pay_date,\
                                    'long_term_per_share':per_share,
                                    'cg_reinvestment_price':reinvestment_price}
                    
                    if divident_type == 'Short Term Cap Gain':
                        capital_gains_dict = {'cg_ex_date':ex_date, 'cg_pay_date':pay_date,\
                                    'short_term_per_share':per_share,\
                                    'cg_reinvestment_price':reinvestment_price}
                    if divident_type == 'Capital Gains':
                        capital_gains_dict = {'cg_ex_date':ex_date, 'cg_pay_date':pay_date,\
                                    'short_term_per_share':per_share,\
                                    'long_term_per_share':per_share,\
                                    'cg_reinvestment_price':reinvestment_price}

                    # dividends.append(divident_dict)
                    capital_gains.append(capital_gains_dict)
            items[j]['dividends'] = dividends
            items[j]['capital_gains'] = capital_gains
            total_items.append(items[j])
        return total_items
