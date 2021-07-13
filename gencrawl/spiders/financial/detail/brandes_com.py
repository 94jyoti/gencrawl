from gencrawl.spiders.financial.financial_detail_spider import FinancialDetailSpider
from gencrawl.spiders.financial.financial_detail_field_mapping import FinancialDetailFieldMapSpider
import scrapy
import re
import pandas as pd
class BrandesComDetail(FinancialDetailFieldMapSpider):
    name = 'financial_detail_brandes_com'

    def get_items_or_req(self, response, default_item=None):
        items = super().get_items_or_req(response, default_item)
        file=open("brandes.html","w")
        file.write(response.text)
        file.close()
        item=items[0]
        #print("tetstttacfascvscvsdhcc",items[0]['minimum_initial_investment'])
        nasdaq_temp=response.xpath('//select[@id="ddlClasses"]//option//@value').extract()
        print(nasdaq_temp)
        for i in range(len(nasdaq_temp)):
        	print(i)
        	if(item['nasdaq_ticker']==nasdaq_temp[i]):
        		item['share_class']=response.xpath('//select[@id="ddlClasses"]//option['+str(i+1)+']//text()').extract()[0]
        
        #=---------------------------
        thead_blocks = response.xpath("//table[@class='fees_and_Expenses']//thead//tr//th[position()>1]/b/text()").extract()
        #print("felmeflemelffmlmlml",thead_blocks)
        for i in range(len(thead_blocks)):
        	thead_blocks[i]=thead_blocks[i].replace("Class","").strip()
        	#print(i)
        #print(thead_blocks)

        tr_blocks = response.xpath("//table[@class='fees_and_Expenses']//tbody//tr")
        #for i in range(len(thead_blocks)):
        #	thead=thead_blocks[i].replace("Class","").strip()
        #	print("theadddd",thead)
        #	print(i)
        for i in items:
        	print(i['share_class'].replace("SHARE",""))
        	if(i['share_class'].replace("SHARE","").strip() in thead_blocks):
        		index_share=thead_blocks.index(i['share_class'].replace("SHARE","").strip())
        		print("indexxxxx",index_share)
        		for tr in tr_blocks:
        			if(index_share==0 and tr.xpath('./td[text()="Maximum Sales Charge (Load)"]').extract_first()):
        				#print("inside seconf iff")
        				item['maximum_sales_charge_full_load']=tr.xpath("./td[text()='Maximum Sales Charge (Load)']/following-sibling::td[1]/span/following::text()[1]").extract_first()
        				#print(item['maximum_sales_charge_full_load'])
        			if(index_share==0 and tr.xpath('./td[text()="Distribution (rule 12b-1) Fees"]').extract_first()):
        				item['fees_total_12b_1']=tr.xpath("./td[text()='Distribution (rule 12b-1) Fees']/following-sibling::td[1]/span/following::text()[1]").extract_first()
        				#print(item['maximum_sales_charge_full_load'])
        				#print("iiiiiiiiii",i)
        			if(index_share==1 and tr.xpath('./td[text()="Maximum Sales Charge (Load)"]').extract_first()):
        				#print("inside seconf iff")
        				item['maximum_sales_charge_full_load']=tr.xpath("./td[text()='Maximum Sales Charge (Load)']/following-sibling::td[2]/span/following::text()[1]").extract_first()
        				#print(item['maximum_sales_charge_full_load'])
        			if(index_share==1 and tr.xpath('./td[text()="Distribution (rule 12b-1) Fees"]').extract_first()):
        				item['fees_total_12b_1']=tr.xpath("./td[text()='Distribution (rule 12b-1) Fees']/following-sibling::td[2]/span/following::text()[1]").extract_first()
        				#print(item['maximum_sales_charge_full_load'])
        				#print("iiiiiiiiii",i)
        
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
        #	print(item)
        #	print(share_class_temp[item].replace("SHARE","").strip())
        #	items[item]['share_class']=share_class_temp[item].replace("SHARE","").strip()
        #return items
    '''
        for i in range(len(share_class_table_list)):
        		if(items[item]['share_class']==share_class_table_list[i].replace("Class","").strip):
        			print("yepppp")
        return items'''