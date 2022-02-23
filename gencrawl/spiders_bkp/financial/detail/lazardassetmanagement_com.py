from gencrawl.spiders.financial.financial_detail_spider import FinancialDetailSpider
from gencrawl.spiders.financial.financial_detail_field_mapping import FinancialDetailFieldMapSpider
import scrapy
import re
from gencrawl.items.financial.financial_detail_item import FinancialDetailItem
from gencrawl.spiders.financial.financial_detail_field_mapping import FinancialDetailFieldMapSpider


class lazardassetmanagementComDetail(FinancialDetailFieldMapSpider):
    name = 'lazardassetmanagement_com'
    def get_items_or_req(self, response, default_item=None):

        meta = response.meta

        items = super().get_items_or_req(response, default_item)

        for item in items:

            capital_gain_list=[]
            dividends_list=[]
            ticker = item['nasdaq_ticker']
            print(ticker)
            #open(ticker+'.html','w',encoding='utf-8').write(response.text)
            
            cg_record_date = response.xpath("(//td[contains(text(),'Record Date')])[1]/following-sibling::td/text()").get()
            cg_pay_date = response.xpath("(//td[contains(text(),'Payable Date')])[1]/following-sibling::td/text()").get()
            cg_ex_date = response.xpath("(//td[contains(text(),'Ex Date')])[1]/following-sibling::td/text()").get()
            cg_record_date = response.xpath("(//td[contains(text(),'Record Date')])[1]/following-sibling::td/text()").get()
            cg_reinvestment_price = response.xpath("(//td[contains(text(),'Reinvest Price')])[1]/following-sibling::td/text()").get()
            ordinary_income = response.xpath("(//td[contains(text(),'Ordinary Income')])[1]/following-sibling::td/text()").get()
            short_term_per_share =""
            long_term_per_share =""
            record_date = cg_record_date

            data_dict1={"cg_ex_date": cg_ex_date, "cg_record_date": cg_record_date, "cg_pay_date": cg_pay_date, "short_term_per_share": short_term_per_share,"long_term_per_share": long_term_per_share, "total_per_share": "", "cg_reinvestment_price": cg_reinvestment_price}

            capital_gain_list.append(data_dict1)

            data_dict2={"ex_date": "", "pay_date": "", "ordinary_income": ordinary_income, "qualified_income": "", "record_date": record_date,"per_share": "", "reinvestment_price": ""}

            dividends_list.append(data_dict2)


            historical_dividends = response.xpath("//table[@class='historical-dividends__table']/tbody")
            block_data=[]
            for tr_block in historical_dividends.xpath("tr"):
                #print(tr_block)
                tr_data = []
                for td_block in tr_block.xpath("td"):
                    td_value = td_block.xpath("text()").get()
                    tr_data.append(td_value)
                #print(tr_data)
                block_data.append(tr_data)

            print("block_data:",block_data)

            for data in block_data:
                cg_record_date =data[0]
                cg_ex_date =data[2]
                cg_pay_date =data[1]
                short_term_per_share =data[6]
                long_term_per_share =data[7]
                cg_reinvestment_price = data[4]

                record_date = data[0]
                ordinary_income = data[5]

                data_dict1={"cg_ex_date": cg_ex_date, "cg_record_date": cg_record_date, "cg_pay_date": cg_pay_date, "short_term_per_share": short_term_per_share,"long_term_per_share": long_term_per_share, "total_per_share": "", "cg_reinvestment_price": cg_reinvestment_price}

                

                data_dict2={"ex_date": "", "pay_date": "", "ordinary_income": ordinary_income, "qualified_income": "", "record_date": record_date,"per_share": "", "reinvestment_price": ""}
                capital_gain_list.append(data_dict1)
                dividends_list.append(data_dict2)

            item['capital_gains']=capital_gain_list
            item['dividends']=dividends_list

            yield self.generate_item(item, FinancialDetailItem)
