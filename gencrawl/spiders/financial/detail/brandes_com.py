from gencrawl.spiders.financial.financial_detail_spider import FinancialDetailSpider
from gencrawl.spiders.financial.financial_detail_field_mapping import FinancialDetailFieldMapSpider
import scrapy
import re
import pandas as pd
class BrandesComDetail(FinancialDetailFieldMapSpider):
    name = 'financial_detail_brandes_com'

    def get_items_or_req(self, response, default_item=None):
        items = super().get_items_or_req(response, default_item)
        item=items[0]
        nasdaq_temp=response.xpath('//select[@id="ddlClasses"]//option//@value').extract()
        for i in range(len(nasdaq_temp)):
            if(item['nasdaq_ticker']==nasdaq_temp[i]):
                item['share_class']=response.xpath('//select[@id="ddlClasses"]//option['+str(i+1)+']//text()').extract()[0]
            item['dividend_frequency']=response.xpath('//span[contains(text(),"Dividend Frequency")]//following-sibling::em//text()').extract()[0]
            item['benchmarks']=response.xpath('//span[contains(text(),"fund benchmark")]//b//text()').extract()
        #=---------------------------
        thead_blocks = response.xpath("//table[@class='fees_and_Expenses']//thead//tr//th[position()>1]/b/text()").extract()
        for i in range(len(thead_blocks)):
            thead_blocks[i]=thead_blocks[i].replace("Class","").strip()
        if(thead_blocks==[]):
            thead_blocks=""
        tr_blocks = response.xpath("//table[@class='fees_and_Expenses']//tbody//tr")
        for i in items:
            i['sec_yield_date_30_day']=(response.xpath('//div[@class="cont_info"]//span[contains(text(),"SEC 30 Day Yield (subsidized)")]/text()').extract()[0]).split("as of")[-1]
            i['sec_yield_30_day']=response.xpath('//div[@class="cont_info"]//span[contains(text(),"SEC 30 Day Yield (subsidized)")]//following-sibling::strong/text()').extract()[0]
            i['sec_yield_without_waivers_30_day']=response.xpath('//div[@class="cont_info"]//span[contains(text(),"SEC 30 Day Yield (unsubsidized)")]//following-sibling::strong/text()').extract()[0]
            i['sec_yield_without_waivers_date_30_day']=(response.xpath('//div[@class="cont_info"]//span[contains(text(),"SEC 30 Day Yield (unsubsidized)")]/text()').extract()[0]).split("as of")[-1]
            if(i['share_class']==[]):
                i['share_class']=""
            if(i['share_class'].replace("SHARE","").strip() in thead_blocks):
                index_share=thead_blocks.index(i['share_class'].replace("SHARE","").strip())
                for tr in tr_blocks:
                    if(index_share==0 and tr.xpath('./td[contains(text(),"Maximum Sales Charge (Load)")]').extract_first()):
                        item['maximum_sales_charge_full_load']=tr.xpath("./td[contains(text(),'Maximum Sales Charge (Load)')]/following-sibling::td[1]/span/following::text()[1]").extract_first()
                    if(index_share==0 and tr.xpath('./td[contains(text(),"Distribution (rule 12b-1) Fees")]').extract_first()):
                        item['fees_total_12b_1']=tr.xpath("./td[contains(text(),'Distribution (rule 12b-1) Fees')]/following-sibling::td[1]/span/following::text()[1]").extract_first()
                    if(index_share==1 and tr.xpath('./td[contains(text(),"Maximum Sales Charge (Load)")]').extract_first()):
                        item['maximum_sales_charge_full_load']=tr.xpath("./td[contains(text(),'Maximum Sales Charge (Load)')]/following-sibling::td[2]/span/following::text()[1]").extract_first()
                    if(index_share==2 and tr.xpath('./td[contains(text(),"Maximum Sales Charge (Load)")]').extract_first()):
                        item['maximum_sales_charge_full_load']=tr.xpath("./td[contains(text(),'Maximum Sales Charge (Load)')]/following-sibling::td[3]/span/following::text()[1]").extract_first()
                    if(index_share==3 and tr.xpath('./td[contains(text(),"Maximum Sales Charge (Load)")]').extract_first()):
                        item['maximum_sales_charge_full_load']=tr.xpath("./td[contains(text(),'Maximum Sales Charge (Load)')]/following-sibling::td[4]/span/following::text()[1]").extract_first()
                    if(index_share==4 and tr.xpath('./td[contains(text(),"Maximum Sales Charge (Load)")]').extract_first()):
                        item['maximum_sales_charge_full_load']=tr.xpath("./td[contains(text(),'Maximum Sales Charge (Load)')]/following-sibling::td[5]/span/following::text()[1]").extract_first()
                    if(index_share==1 and tr.xpath('./td[text()="Distribution (rule 12b-1) Fees"]').extract_first()):
                        item['fees_total_12b_1']=tr.xpath("./td[text()='Distribution (rule 12b-1) Fees']/following-sibling::td[2]/span/following::text()[1]").extract_first()
                    if(index_share==2 and tr.xpath('./td[text()="Distribution (rule 12b-1) Fees"]').extract_first()):
                        item['fees_total_12b_1']=tr.xpath("./td[text()='Distribution (rule 12b-1) Fees']/following-sibling::td[3]/span/following::text()[1]").extract_first()
                    if(index_share==3 and tr.xpath('./td[text()="Distribution (rule 12b-1) Fees"]').extract_first()):
                        item['fees_total_12b_1']=tr.xpath("./td[text()='Distribution (rule 12b-1) Fees']/following-sibling::td[4]/span/following::text()[1]").extract_first()
                    if(index_share==4 and tr.xpath('./td[text()="Distribution (rule 12b-1) Fees"]').extract_first()):
                        item['fees_total_12b_1']=tr.xpath("./td[text()='Distribution (rule 12b-1) Fees']/following-sibling::td[5]/span/following::text()[1]").extract_first()
                    #---------------------------------------------------------------------------------------------------------
                    
                    
                    if(index_share==0 and tr.xpath('./td[text()="Total Other Expenses"]').extract_first()):
                        item['other_expenses']=tr.xpath("./td[text()='Total Other Expenses']/following-sibling::td[1]/span/following::text()[1]").extract_first()
                    if(index_share==1 and tr.xpath('./td[text()="Total Other Expenses"]').extract_first()):
                        item['other_expenses']=tr.xpath("./td[text()='Total Other Expenses']/following-sibling::td[2]/span/following::text()[1]").extract_first()
                    if(index_share==2 and tr.xpath('./td[text()="Total Other Expenses"]').extract_first()):
                        item['other_expenses']=tr.xpath("./td[text()='Total Other Expenses']/following-sibling::td[3]/span/following::text()[1]").extract_first()
                    if(index_share==3 and tr.xpath('./td[text()="Total Other Expenses"]').extract_first()):
                        item['other_expenses']=tr.xpath("./td[text()='Total Other Expenses']/following-sibling::td[4]/span/following::text()[1]").extract_first()
                    if(index_share==4 and tr.xpath('./td[text()="Total Other Expenses"]').extract_first()):
                        item['other_expenses']=tr.xpath("./td[text()='Total Other Expenses']/following-sibling::td[5]/span/following::text()[1]").extract_first()
                    #-------------------------------------------------------------------------------
                    if(index_share==0 and tr.xpath('./td[text()="Total Annual Fund Operating Expenses "or text()="Total Annual Fund Operating Expenses"]').extract_first()):
                        item['total_expense_gross']=tr.xpath("./td[text()='Total Annual Fund Operating Expenses 'or text()='Total Annual Fund Operating Expenses']/following-sibling::td[1]/span/following::text()[1]").extract_first()
                    if(index_share==1 and tr.xpath('./td[text()="Total Annual Fund Operating Expenses "or text()="Total Annual Fund Operating Expenses"]').extract_first()):
                        item['total_expense_gross']=tr.xpath("./td[text()='Total Annual Fund Operating Expenses 'or text()='Total Annual Fund Operating Expenses']/following-sibling::td[2]/span/following::text()[1]").extract_first()
                    if(index_share==2 and tr.xpath('./td[text()="Total Annual Fund Operating Expenses "or text()="Total Annual Fund Operating Expenses"]').extract_first()):
                        item['total_expense_gross']=tr.xpath("./td[text()='Total Annual Fund Operating Expenses 'or text()='Total Annual Fund Operating Expenses']/following-sibling::td[3]/span/following::text()[1]").extract_first()
                    if(index_share==3 and tr.xpath('./td[text()="Total Annual Fund Operating Expenses "or text()="Total Annual Fund Operating Expenses"]').extract_first()):
                        item['total_expense_gross']=tr.xpath("./td[text()='Total Annual Fund Operating Expenses 'or text()='Total Annual Fund Operating Expenses']/following-sibling::td[4]/span/following::text()[1]").extract_first()
                    if(index_share==4 and tr.xpath('./td[text()="Total Annual Fund Operating Expenses "or text()="Total Annual Fund Operating Expenses"]').extract_first()):
                        item['total_expense_gross']=tr.xpath("./td[text()='Total Annual Fund Operating Expenses 'or text()='Total Annual Fund Operating Expenses']/following-sibling::td[5]/span/following::text()[1]").extract_first()
                    #=-------------------------
                    if(index_share==0 and tr.xpath('./td[contains(text(),"Fee Waiver/Expense Reimbursement")or contains(text(),"Fee Waiver and/or Expense Reimbursement")]').extract_first()):
                        item['expense_waivers']=tr.xpath("./td[contains(text(),'Fee Waiver/Expense Reimbursement')or contains(text(),'Fee Waiver and/or Expense Reimbursement')]/following-sibling::td[1]/span/following::text()[1]").extract_first()

                    if(index_share==1 and tr.xpath('./td[contains(text(),"Fee Waiver/Expense Reimbursement")or contains(text(),"Fee Waiver and/or Expense Reimbursement")]').extract_first()):
                        item['expense_waivers']=tr.xpath("./td[contains(text(),'Fee Waiver/Expense Reimbursement')or contains(text(),'Fee Waiver and/or Expense Reimbursement')]/following-sibling::td[2]/span/following::text()[1]").extract_first()

                    if(index_share==2 and tr.xpath('./td[contains(text(),"Fee Waiver/Expense Reimbursement")or contains(text(),"Fee Waiver and/or Expense Reimbursement")]').extract_first()):
                        item['expense_waivers']=tr.xpath("./td[contains(text(),'Fee Waiver/Expense Reimbursement')or contains(text(),'Fee Waiver and/or Expense Reimbursement')]/following-sibling::td[3]/span/following::text()[1]").extract_first()

                    if(index_share==3 and tr.xpath('./td[contains(text(),"Fee Waiver/Expense Reimbursement")or contains(text(),"Fee Waiver and/or Expense Reimbursement")]').extract_first()):
                        item['expense_waivers']=tr.xpath("./td[contains(text(),'Fee Waiver/Expense Reimbursement')or contains(text(),'Fee Waiver and/or Expense Reimbursement')]/following-sibling::td[4]/span/following::text()[1]").extract_first()

                    if(index_share==4 and tr.xpath('./td[contains(text(),"Fee Waiver/Expense Reimbursement")or contains(text(),"Fee Waiver and/or Expense Reimbursement")]').extract_first()):
                        item['expense_waivers']=tr.xpath("./td[contains(text(),'Fee Waiver/Expense Reimbursement')or contains(text(),'Fee Waiver and/or Expense Reimbursement')]/following-sibling::td[5]/span/following::text()[1]").extract_first()
                    #=-------------------------
                    if(index_share==0 and tr.xpath('./td[contains(text(),"Net Annual Fund Operating Expenses")or contains(text(),"Expenses After Fee Waiver")]').extract_first()):
                        item['total_expense_net']=tr.xpath("./td[contains(text(),'Net Annual Fund Operating Expenses')or contains(text(),'Expenses After Fee Waiver')]/following-sibling::td[1]/span/following::text()[1]").extract_first()

                    if(index_share==1 and tr.xpath('./td[contains(text(),"Net Annual Fund Operating Expenses")or contains(text(),"Expenses After Fee Waiver")]').extract_first()):
                        item['total_expense_net']=tr.xpath("./td[contains(text(),'Net Annual Fund Operating Expenses')or contains(text(),'Expenses After Fee Waiver')]/following-sibling::td[2]/span/following::text()[1]").extract_first()

                    if(index_share==2 and tr.xpath('./td[contains(text(),"Net Annual Fund Operating Expenses")or contains(text(),"Expenses After Fee Waiver")]').extract_first()):
                        item['total_expense_net']=tr.xpath("./td[contains(text(),'Net Annual Fund Operating Expenses')or contains(text(),'Expenses After Fee Waiver')]/following-sibling::td[3]/span/following::text()[1]").extract_first()

                    if(index_share==3 and tr.xpath('./td[contains(text(),"Net Annual Fund Operating Expenses")or contains(text(),"Expenses After Fee Waiver")]').extract_first()):
                        item['total_expense_net']=tr.xpath("./td[contains(text(),'Net Annual Fund Operating Expenses')or contains(text(),'Expenses After Fee Waiver')]/following-sibling::td[4]/span/following::text()[1]").extract_first()
                    if(index_share==4 and tr.xpath('./td[contains(text(),"Net Annual Fund Operating Expenses")or contains(text(),"Expenses After Fee Waiver")]').extract_first()):
                        item['total_expense_net']=tr.xpath("./td[contains(text(),'Net Annual Fund Operating Expenses')or contains(text(),'Expenses After Fee Waiver')]/following-sibling::td[5]/span/following::text()[1]").extract_first()
                    #------------------------------------------------------------------------------------------------------
                    try:
                        if(index_share==0 and tr.xpath('./td[contains(text(),"Deferred")]').extract_first()):
                            item['deferred_sales_charge']=tr.xpath("./td[contains(text(),'Deferred')]/following-sibling::td[1]/span/following::text()[1]").extract_first()

                        if(index_share==1 and tr.xpath('./td[contains(text(),"Deferred")]').extract_first()):
                            item['deferred_sales_charge']=tr.xpath("./td[contains(text(),'Deferred')]/following-sibling::td[1]/span/following::text()[1]").extract_first()

                        if(index_share==2 and tr.xpath('./td[contains(text(),"Deferred")]').extract_first()):
                            item['deferred_sales_charge']=tr.xpath("./td[contains(text(),'Deferred')]/following-sibling::td[1]/span/following::text()[1]").extract_first()

                        if(index_share==3 and tr.xpath('./td[contains(text(),"Deferred")]').extract_first()):
                            item['deferred_sales_charge']=tr.xpath("./td[contains(text(),'Deferred')]/following-sibling::td[1]/span/following::text()[1]").extract_first()

                        if(index_share==4 and tr.xpath('./td[contains(text(),"Deferred")]').extract_first()):
                            item['deferred_sales_charge']=tr.xpath("./td[contains(text(),'Deferred')]/following-sibling::td[1]/span/following::text()[1]").extract_first()
                    except:
                        pass
        return items