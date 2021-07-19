from gencrawl.spiders.financial.financial_detail_spider import FinancialDetailSpider
from gencrawl.spiders.financial.financial_detail_field_mapping import FinancialDetailFieldMapSpider
import scrapy
import re
import pandas as pd
class BrandesComDetail(FinancialDetailFieldMapSpider):
    name = 'financial_detail_brandes_com'

    def get_items_or_req(self, response, default_item=None):
        items = super().get_items_or_req(response, default_item)
        print(items[0])
        file=open("brandes.html","w")
        file.write(response.text)
        file.close()
        item=items[0]
        #print("tetstttacfascvscvsdhcc",items[0]['minimum_initial_investment'])
        nasdaq_temp=response.xpath('//select[@id="ddlClasses"]//option//@value').extract()
        for i in range(len(nasdaq_temp)):
            print(i)
            if(item['nasdaq_ticker']==nasdaq_temp[i]):
                item['share_class']=response.xpath('//select[@id="ddlClasses"]//option['+str(i+1)+']//text()').extract()[0]
            item['dividend_frequency']=response.xpath('//span[contains(text(),"Dividend Frequency")]//following-sibling::em//text()').extract()[0]
            item['benchmarks']=response.xpath('//span[contains(text(),"fund benchmark")]//b//text()').extract()
        #=---------------------------
        thead_blocks = response.xpath("//table[@class='fees_and_Expenses']//thead//tr//th[position()>1]/b/text()").extract()
        
        #print("felmeflemelffmlmlml",thead_blocks)
        for i in range(len(thead_blocks)):
            thead_blocks[i]=thead_blocks[i].replace("Class","").strip()
            #print(i)
        print("ververvevevevvrfvvvrvv",thead_blocks)
        if(thead_blocks==[]):
            thead_blocks=""
        tr_blocks = response.xpath("//table[@class='fees_and_Expenses']//tbody//tr")
        #for i in range(len(thead_blocks)):
        #   thead=thead_blocks[i].replace("Class","").strip()
        #   print("theadddd",thead)
        #   print(i)    
        #sec_30=response.xpath('//div[@class="cont_info"]//span[contains(text(),"SEC 30 Day Yield (subsidized)")]//following-sibling::strong/text()').extract()[0]
        for i in items:
            i['sec_yield_date_30_day']=(response.xpath('//div[@class="cont_info"]//span[contains(text(),"SEC 30 Day Yield (subsidized)")]/text()').extract()[0]).split("as of")[-1]
            #i['sec_yield_30_day']
            i['sec_yield_30_day']=response.xpath('//div[@class="cont_info"]//span[contains(text(),"SEC 30 Day Yield (subsidized)")]//following-sibling::strong/text()').extract()[0]
            i['sec_yield_without_waivers_30_day']=response.xpath('//div[@class="cont_info"]//span[contains(text(),"SEC 30 Day Yield (unsubsidized)")]//following-sibling::strong/text()').extract()[0]
            i['sec_yield_without_waivers_date_30_day']=(response.xpath('//div[@class="cont_info"]//span[contains(text(),"SEC 30 Day Yield (unsubsidized)")]/text()').extract()[0]).split("as of")[-1]
            if(i['share_class']==[]):
                i['share_class']=""
            #print(i['share_class'].replace("SHARE",""))
            if(i['share_class'].replace("SHARE","").strip() in thead_blocks):
                index_share=thead_blocks.index(i['share_class'].replace("SHARE","").strip())
                print("indexxxxx",index_share)
                for tr in tr_blocks:
                    if(index_share==0 and tr.xpath('./td[contains(text(),"Maximum Sales Charge (Load)")]').extract_first()):
                        #print("inside seconf iff")
                        item['maximum_sales_charge_full_load']=tr.xpath("./td[contains(text(),'Maximum Sales Charge (Load)')]/following-sibling::td[1]/span/following::text()[1]").extract_first()
                        #print(item['maximum_sales_charge_full_load'])
                    if(index_share==0 and tr.xpath('./td[contains(text(),"Distribution (rule 12b-1) Fees")]').extract_first()):
                        item['fees_total_12b_1']=tr.xpath("./td[contains(text(),'Distribution (rule 12b-1) Fees')]/following-sibling::td[1]/span/following::text()[1]").extract_first()
                        #print(item['maximum_sales_charge_full_load'])
                        #print("iiiiiiiiii",i)
                    if(index_share==1 and tr.xpath('./td[contains(text(),"Maximum Sales Charge (Load)")]').extract_first()):
                        #print("inside seconf iff")
                        item['maximum_sales_charge_full_load']=tr.xpath("./td[contains(text(),'Maximum Sales Charge (Load)')]/following-sibling::td[2]/span/following::text()[1]").extract_first()
                        #print(item['maximum_sales_charge_full_load'])
                    if(index_share==2 and tr.xpath('./td[contains(text(),"Maximum Sales Charge (Load)")]').extract_first()):
                        #print("inside seconf iff")
                        item['maximum_sales_charge_full_load']=tr.xpath("./td[contains(text(),'Maximum Sales Charge (Load)')]/following-sibling::td[3]/span/following::text()[1]").extract_first()
                        #print(item['maximum_sales_charge_full_load'])
                    if(index_share==3 and tr.xpath('./td[contains(text(),"Maximum Sales Charge (Load)")]').extract_first()):
                        #print("inside seconf iff")
                        item['maximum_sales_charge_full_load']=tr.xpath("./td[contains(text(),'Maximum Sales Charge (Load)')]/following-sibling::td[4]/span/following::text()[1]").extract_first()
                        #print(item['maximum_sales_charge_full_load'])
                    if(index_share==4 and tr.xpath('./td[contains(text(),"Maximum Sales Charge (Load)")]').extract_first()):
                        #print("inside seconf iff")
                        item['maximum_sales_charge_full_load']=tr.xpath("./td[contains(text(),'Maximum Sales Charge (Load)')]/following-sibling::td[5]/span/following::text()[1]").extract_first()
                        #print(item['maximum_sales_charge_full_load'])
                    if(index_share==1 and tr.xpath('./td[text()="Distribution (rule 12b-1) Fees"]').extract_first()):
                        item['fees_total_12b_1']=tr.xpath("./td[text()='Distribution (rule 12b-1) Fees']/following-sibling::td[2]/span/following::text()[1]").extract_first()
                        #print(item['maximum_sales_charge_full_load'])
                        #print("iiiiiiiiii",i)
                    if(index_share==2 and tr.xpath('./td[text()="Distribution (rule 12b-1) Fees"]').extract_first()):
                        item['fees_total_12b_1']=tr.xpath("./td[text()='Distribution (rule 12b-1) Fees']/following-sibling::td[3]/span/following::text()[1]").extract_first()
                        #print(item['maximum_sales_charge_full_load'])
                    if(index_share==3 and tr.xpath('./td[text()="Distribution (rule 12b-1) Fees"]').extract_first()):
                        item['fees_total_12b_1']=tr.xpath("./td[text()='Distribution (rule 12b-1) Fees']/following-sibling::td[4]/span/following::text()[1]").extract_first()
                        #print(item['maximum_sales_charge_full_load'])
                        #print("iiiiiiiiii",i)
                        #print("iiiiiiiiii",i)
                    if(index_share==4 and tr.xpath('./td[text()="Distribution (rule 12b-1) Fees"]').extract_first()):
                        item['fees_total_12b_1']=tr.xpath("./td[text()='Distribution (rule 12b-1) Fees']/following-sibling::td[5]/span/following::text()[1]").extract_first()
                        #print(item['maximum_sales_charge_full_load'])
                        #print("iiiiiiiiii",i)
                    #---------------------------------------------------------------------------------------------------------
                    
                    
                    if(index_share==0 and tr.xpath('./td[text()="Total Other Expenses"]').extract_first()):
                        item['other_expenses']=tr.xpath("./td[text()='Total Other Expenses']/following-sibling::td[1]/span/following::text()[1]").extract_first()
                        print(item['other_expenses'])
                        #print("iiiiiiiiii",i)
                    #if(index_share==0 and  tr.xpath('./td[text()="Other Expenses "]').extract_first() ):
                     #   item['other_expenses']=tr.xpath("./td[text()='Other Expenses ']/following-sibling::td[1]/span/following::text()[1]").extract_first()
                    if(index_share==1 and tr.xpath('./td[text()="Total Other Expenses"]').extract_first()):
                        item['other_expenses']=tr.xpath("./td[text()='Total Other Expenses']/following-sibling::td[2]/span/following::text()[1]").extract_first()
                        #print(item['maximum_sales_charge_full_load'])
                        #print("iiiiiiiiii",i)
                    if(index_share==2 and tr.xpath('./td[text()="Total Other Expenses"]').extract_first()):
                        item['other_expenses']=tr.xpath("./td[text()='Total Other Expenses']/following-sibling::td[3]/span/following::text()[1]").extract_first()
                        #print(item['maximum_sales_charge_full_load'])
                        #print("iiiiiiiiii",i)
                    if(index_share==3 and tr.xpath('./td[text()="Total Other Expenses"]').extract_first()):
                        item['other_expenses']=tr.xpath("./td[text()='Total Other Expenses']/following-sibling::td[4]/span/following::text()[1]").extract_first()
                        #print(item['maximum_sales_charge_full_load'])
                    if(index_share==4 and tr.xpath('./td[text()="Total Other Expenses"]').extract_first()):
                        item['other_expenses']=tr.xpath("./td[text()='Total Other Expenses']/following-sibling::td[5]/span/following::text()[1]").extract_first()
                        #print(item['maximum_sales_charge_full_load'])
                        #print("iiiiiiiiii",i)
                    #-------------------------------------------------------------------------------
                    if(index_share==0 and tr.xpath('./td[text()="Total Annual Fund Operating Expenses "or text()="Total Annual Fund Operating Expenses"]').extract_first()):
                        item['total_expense_gross']=tr.xpath("./td[text()='Total Annual Fund Operating Expenses 'or text()='Total Annual Fund Operating Expenses']/following-sibling::td[1]/span/following::text()[1]").extract_first()
                        #print(item['maximum_sales_charge_full_load'])
                        #print("iiiiiiiiii",i)
                    if(index_share==1 and tr.xpath('./td[text()="Total Annual Fund Operating Expenses "or text()="Total Annual Fund Operating Expenses"]').extract_first()):
                        item['total_expense_gross']=tr.xpath("./td[text()='Total Annual Fund Operating Expenses 'or text()='Total Annual Fund Operating Expenses']/following-sibling::td[2]/span/following::text()[1]").extract_first()
                        #print(item['maximum_sales_charge_full_load'])
                        #print("iiiiiiiiii",i)
                    if(index_share==2 and tr.xpath('./td[text()="Total Annual Fund Operating Expenses "or text()="Total Annual Fund Operating Expenses"]').extract_first()):
                        item['total_expense_gross']=tr.xpath("./td[text()='Total Annual Fund Operating Expenses 'or text()='Total Annual Fund Operating Expenses']/following-sibling::td[3]/span/following::text()[1]").extract_first()
                        #print(item['maximum_sales_charge_full_load'])
                        #print("iiiiiiiiii",i)
                    if(index_share==3 and tr.xpath('./td[text()="Total Annual Fund Operating Expenses "or text()="Total Annual Fund Operating Expenses"]').extract_first()):
                        item['total_expense_gross']=tr.xpath("./td[text()='Total Annual Fund Operating Expenses 'or text()='Total Annual Fund Operating Expenses']/following-sibling::td[4]/span/following::text()[1]").extract_first()
                        #print(item['maximum_sales_charge_full_load'])
                        #print("iiiiiiiiii",i)
                    if(index_share==4 and tr.xpath('./td[text()="Total Annual Fund Operating Expenses "or text()="Total Annual Fund Operating Expenses"]').extract_first()):
                        item['total_expense_gross']=tr.xpath("./td[text()='Total Annual Fund Operating Expenses 'or text()='Total Annual Fund Operating Expenses']/following-sibling::td[5]/span/following::text()[1]").extract_first()
                        #print(item['maximum_sales_charge_full_load'])
                        #print("iiiiiiiiii",i)
                    #=-------------------------
                    if(index_share==0 and tr.xpath('./td[contains(text(),"Fee Waiver/Expense Reimbursement")or contains(text(),"Fee Waiver and/or Expense Reimbursement")]').extract_first()):
                        item['expense_waivers']=tr.xpath("./td[contains(text(),'Fee Waiver/Expense Reimbursement')or contains(text(),'Fee Waiver and/or Expense Reimbursement')]/following-sibling::td[1]/span/following::text()[1]").extract_first()
                        #print(item['maximum_sales_charge_full_load'])
                        #print("iiiiiiiiii",i)
                    if(index_share==1 and tr.xpath('./td[contains(text(),"Fee Waiver/Expense Reimbursement")or contains(text(),"Fee Waiver and/or Expense Reimbursement")]').extract_first()):
                        item['expense_waivers']=tr.xpath("./td[contains(text(),'Fee Waiver/Expense Reimbursement')or contains(text(),'Fee Waiver and/or Expense Reimbursement')]/following-sibling::td[2]/span/following::text()[1]").extract_first()
                        #print(item['maximum_sales_charge_full_load'])
                        #print("iiiiiiiiii",i)
                    if(index_share==2 and tr.xpath('./td[contains(text(),"Fee Waiver/Expense Reimbursement")or contains(text(),"Fee Waiver and/or Expense Reimbursement")]').extract_first()):
                        item['expense_waivers']=tr.xpath("./td[contains(text(),'Fee Waiver/Expense Reimbursement')or contains(text(),'Fee Waiver and/or Expense Reimbursement')]/following-sibling::td[3]/span/following::text()[1]").extract_first()
                        #print(item['maximum_sales_charge_full_load'])
                        #print("iiiiiiiiii",i)
                    if(index_share==3 and tr.xpath('./td[contains(text(),"Fee Waiver/Expense Reimbursement")or contains(text(),"Fee Waiver and/or Expense Reimbursement")]').extract_first()):
                        item['expense_waivers']=tr.xpath("./td[contains(text(),'Fee Waiver/Expense Reimbursement')or contains(text(),'Fee Waiver and/or Expense Reimbursement')]/following-sibling::td[4]/span/following::text()[1]").extract_first()
                        #print(item['maximum_sales_charge_full_load'])
                        #print("iiiiiiiiii",i)
                    if(index_share==4 and tr.xpath('./td[contains(text(),"Fee Waiver/Expense Reimbursement")or contains(text(),"Fee Waiver and/or Expense Reimbursement")]').extract_first()):
                        item['expense_waivers']=tr.xpath("./td[contains(text(),'Fee Waiver/Expense Reimbursement')or contains(text(),'Fee Waiver and/or Expense Reimbursement')]/following-sibling::td[5]/span/following::text()[1]").extract_first()
                        #print(item['maximum_sales_charge_full_load'])
                        #print("iiiiiiiiii",i)
                    #=-------------------------
                    if(index_share==0 and tr.xpath('./td[contains(text(),"Net Annual Fund Operating Expenses")or contains(text(),"Expenses After Fee Waiver")]').extract_first()):
                        item['total_expense_net']=tr.xpath("./td[contains(text(),'Net Annual Fund Operating Expenses')or contains(text(),'Expenses After Fee Waiver')]/following-sibling::td[1]/span/following::text()[1]").extract_first()
                        #print(item['maximum_sales_charge_full_load'])
                        #print("iiiiiiiiii",i)
                    if(index_share==1 and tr.xpath('./td[contains(text(),"Net Annual Fund Operating Expenses")or contains(text(),"Expenses After Fee Waiver")]').extract_first()):
                        item['total_expense_net']=tr.xpath("./td[contains(text(),'Net Annual Fund Operating Expenses')or contains(text(),'Expenses After Fee Waiver')]/following-sibling::td[2]/span/following::text()[1]").extract_first()
                        #print(item['maximum_sales_charge_full_load'])
                        #print("iiiiiiiiii",i)
                    if(index_share==2 and tr.xpath('./td[contains(text(),"Net Annual Fund Operating Expenses")or contains(text(),"Expenses After Fee Waiver")]').extract_first()):
                        item['total_expense_net']=tr.xpath("./td[contains(text(),'Net Annual Fund Operating Expenses')or contains(text(),'Expenses After Fee Waiver')]/following-sibling::td[3]/span/following::text()[1]").extract_first()
                        #print(item['maximum_sales_charge_full_load'])
                        #print("iiiiiiiiii",i)
                    if(index_share==3 and tr.xpath('./td[contains(text(),"Net Annual Fund Operating Expenses")or contains(text(),"Expenses After Fee Waiver")]').extract_first()):
                        item['total_expense_net']=tr.xpath("./td[contains(text(),'Net Annual Fund Operating Expenses')or contains(text(),'Expenses After Fee Waiver')]/following-sibling::td[4]/span/following::text()[1]").extract_first()
                        #print(item['maximum_sales_charge_full_load'])
                        #print("iiiiiiiiii",i)
                    if(index_share==4 and tr.xpath('./td[contains(text(),"Net Annual Fund Operating Expenses")or contains(text(),"Expenses After Fee Waiver")]').extract_first()):
                        item['total_expense_net']=tr.xpath("./td[contains(text(),'Net Annual Fund Operating Expenses')or contains(text(),'Expenses After Fee Waiver')]/following-sibling::td[5]/span/following::text()[1]").extract_first()
                        #print(item['maximum_sales_charge_full_load'])
                        #print("iiiiiiiiii",i
                    #------------------------------------------------------------------------------------------------------
                    try:
                        if(index_share==0 and tr.xpath('./td[contains(text(),"Deferred")]').extract_first()):
                            item['deferred_sales_charge']=tr.xpath("./td[contains(text(),'Deferred')]/following-sibling::td[1]/span/following::text()[1]").extract_first()
                            #print(item['maximum_sales_charge_full_load'])
                            #print("iiiiiiiiii",i)
                        if(index_share==1 and tr.xpath('./td[contains(text(),"Deferred")]').extract_first()):
                            item['deferred_sales_charge']=tr.xpath("./td[contains(text(),'Deferred')]/following-sibling::td[1]/span/following::text()[1]").extract_first()
                            #print(item['maximum_sales_charge_full_load'])
                            #print("iiiiiiiiii",i)
                        if(index_share==2 and tr.xpath('./td[contains(text(),"Deferred")]').extract_first()):
                            item['deferred_sales_charge']=tr.xpath("./td[contains(text(),'Deferred')]/following-sibling::td[1]/span/following::text()[1]").extract_first()
                            #print(item['maximum_sales_charge_full_load'])
                            #print("iiiiiiiiii",i)
                        if(index_share==3 and tr.xpath('./td[contains(text(),"Deferred")]').extract_first()):
                            item['deferred_sales_charge']=tr.xpath("./td[contains(text(),'Deferred')]/following-sibling::td[1]/span/following::text()[1]").extract_first()
                            #print(item['maximum_sales_charge_full_load'])
                            #print("iiiiiiiiii",i)
                        if(index_share==4 and tr.xpath('./td[contains(text(),"Deferred")]').extract_first()):
                            item['deferred_sales_charge']=tr.xpath("./td[contains(text(),'Deferred')]/following-sibling::td[1]/span/following::text()[1]").extract_first()
                            #print(item['maximum_sales_charge_full_load'])
                                        #print("iiiiiiiiii",i
                    except:
                        pass
        return items
        
        
        
        
        '''
        for tr in tr_blocks:
            for i in items:
                print(i)
                index_share=thead_blocks.index(i['share_class'].replace("SHARE","").strip())
                print(index_share)
                #print(thead)
                #print(item['share_class'].replace("SHARE","").strip())
                
                if(index_share==0 and tr.xpath('./td[text()="Maximum Sales Charge (Load)"]').extract_first()):
                    print("inside seconf iff")
                    item['maximum_sales_charge_full_load']=tr.xpath("./td['+str(index+2)+']/span/following::text()[1]").extract_first()
                    print(item['maximum_sales_charge_full_load'])
                if(index_share==0 and tr.xpath('./td[text()="Distribution (rule 12b-1) Fees"]').extract_first()):
                        item['fees_total_12b_1']=tr.xpath("./td['+str(index+2)+']/span/following::text()[1]").extract_first()
                        print(item['maximum_sales_charge_full_load'])
                        print("iiiiiiiiii",i)
                if(index_share==1 and tr.xpath('./td[text()="Maximum Sales Charge (Load)"]').extract_first()):
                    print("inside seconf iff")
                    item['maximum_sales_charge_full_load']=tr.xpath("./td['+str(index+3)+']/span/following::text()[1]").extract_first()
                    print(item['maximum_sales_charge_full_load'])
                if(index_share==1 and tr.xpath('./td[text()="Distribution (rule 12b-1) Fees"]').extract_first()):
                        item['fees_total_12b_1']=tr.xpath("./td['+str(index+3)+']/span/following::text()[1]").extract_first()
                        print(item['maximum_sales_charge_full_load'])
                        print("iiiiiiiiii",i)'''
        #print(items[0])
        #no_of_items=len(items)
        #print(no_of_items)
        #share_class_temp=response.xpath('//select[@id="ddlClasses"]//option//text()').extract()
        #print(share_class_temp)
        #share_class_table_list=response.xpath('//table[@class="fees_and_Expenses"]/thead/tr/th[position()>1]/b/text()').extract()
        #for item in range(len(items)):
        #   print(item)
        #   print(share_class_temp[item].replace("SHARE","").strip())
        #   items[item]['share_class']=share_class_temp[item].replace("SHARE","").strip()
        #return items
    '''
        for i in range(len(share_class_table_list)):
                if(items[item]['share_class']==share_class_table_list[i].replace("Class","").strip):
                    print("yepppp")
        return items'''