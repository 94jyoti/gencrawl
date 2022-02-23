from gencrawl.spiders.financial.financial_detail_spider import FinancialDetailSpider
from gencrawl.spiders.financial.financial_detail_field_mapping import FinancialDetailFieldMapSpider
from gencrawl.spiders.hospital.hospital_detail_spider import HospitalDetailSpider
import scrapy
import re


class VaneckComDetail(FinancialDetailSpider):
    name = 'financial_detail_vaneck_com'

    def get_items_or_req(self, response, default_item=None):
        items = super().get_items_or_req(response, default_item)
        fee_url = response.url + 'fees-minimums'
        meta = response.meta
        meta['items'] = items
        resp = self.make_request(fee_url, callback=self.parse_fee, method='SELENIUM', meta=meta)
        return resp
    

    def parse_fee(self, response):
        items = response.meta['items']
        share_class = items[0]['share_class'].strip()
        
        all_share_classes = ''.join(response.xpath(\
                                "//h2[contains(text(),'Fees & Charges')]/following-sibling::table[1]//tr/td[1]/text()"\
                                ).extract()).replace('\n','').strip().split()
        share_class_pos = all_share_classes.index(share_class.replace('Class','').strip())
        
        all_max_sales_charges = ''.join(response.xpath(\
                                "//h2[contains(text(),'Fees & Charges')]/following-sibling::table[1]//tr/td[3]/text()"\
                                ).extract()).replace('\n','').strip().split()

        items[0]['maximum_sales_charge_full_load'] = all_max_sales_charges[share_class_pos]


        all_max_differed_sales_charges = ''.join(response.xpath(\
                                "//h2[contains(text(),'Fees & Charges')]/following-sibling::table[1]//tr/td[4]/text()"\
                                ).extract()).replace('\n','').strip().split()
        items[0]['deferred_sales_charge'] = all_max_differed_sales_charges[share_class_pos]

        all_svc_fee_12_bb1 = ''.join(response.xpath(\
                                "//h2[contains(text(),'Fees & Charges')]/following-sibling::table[1]//tr/td[5]/text()"\
                                ).extract()).replace('\n','').strip().split()
        items[0]['fees_total_12b_1'] = all_svc_fee_12_bb1[share_class_pos]

        total_share_rows_data = ''.join(response.xpath("//tr[td[contains(text(),'Shares')]]/td/text()"\
                                    ).extract()).replace('\n','').strip().split('Class')
        del(total_share_rows_data[0])
        
        for item in total_share_rows_data:
            if share_class.replace('Class','').strip() in item.strip():
                investment_data = re.findall(r'Shares(.*?\d+\s).*?(\$*\d+\s)',\
                                                        total_share_rows_data[0])

                items[0]['minimum_initial_investment'] = investment_data[0][0].strip()
                items[0]['minimum_additional_investment'] = investment_data[0][1].strip()

        all_mgmt_fees = response.xpath("//td[contains(text(),'Management Fees')]/following-sibling::td/text()").extract()
        items[0]['management_fee'] = all_mgmt_fees[share_class_pos].replace('\n','').strip()
        
        waiver = response.xpath("//td[contains(text(),'After Fee Waiver')]/following-sibling::td/text()").extract()
        items[0]['annual_fund_operating_expenses_after_fee_waiver'] = waiver[share_class_pos].replace('\n','').strip()

        expense_waivers = response.xpath("//td[contains(text(),'Waived')]/following-sibling::td/text()").extract()
        items[0]['expense_waivers'] = expense_waivers[share_class_pos].replace('\n','').strip()
        
        meta = response.meta
        meta['items'] = items
        fund_mgr_url = response.url.replace('fees-minimums','investment-team')
        
        resp2 = self.make_request(fund_mgr_url, callback=self.parse_fund_manager, method='SELENIUM', meta=meta)
        yield resp2


    def parse_fund_manager(self, response):
        fund_manager_list=[]
        fund_manager_list1=[]
        fund_manager_list2=[]
        items = response.meta['items']
        try:
            temp_fund_mgr_lst = response.xpath(\
                            "//li[contains(@class , 'hardAssetsItem')]//h4/text()"\
                            ).extract()
        except Exception as e:
            temp_fund_mgr_lst = []

        try:
            temp_fund_mgr_exp_list = response.xpath(\
                            "//li[contains(text() , 'Industry Experience ')]/text()"\
                            ).extract()
        except Exception as e:
            temp_fund_mgr_exp_list = []

        try:
            fund_manager_years_of_experience_with_fund_lst = response.xpath(\
                            "//li[contains(text() , 'Industry Experience ')]/following-sibling::li[1]/text()"\
                            ).extract()
        except Exception as e:
            fund_manager_years_of_experience_with_fund_lst = []
        
        for i in range(len(temp_fund_mgr_lst)):
            data_dict={"fund_manager": "","fund_manager_years_of_experience_in_industry":"","fund_manager_years_of_experience_with_fund": ""}
            if 'Deputy Portfolio Manager' in temp_fund_mgr_lst[i]:
                temp_fund_mgr = temp_fund_mgr_lst[i].split('Deputy Portfolio Manager')[0].strip()
                # fund_mgr = re.sub(r'.,$','',temp_fund_mgr)
                pos = temp_fund_mgr.rfind(',')
                fund_mgr = temp_fund_mgr[:pos]
                data_dict['fund_manager'] = fund_mgr
                data_dict['fund_manager_years_of_experience_in_industry'] = temp_fund_mgr_exp_list[i].replace(\
                                                                                'Industry Experience Since','').replace(\
                                                                                'Industry Experience since','').strip()
                data_dict['fund_manager_years_of_experience_with_fund'] = fund_manager_years_of_experience_with_fund_lst[i].replace(\
                                                                                'Joined VanEck in','').strip()
            
            elif 'Portfolio Manager' in temp_fund_mgr_lst[i]:
                temp_fund_mgr = temp_fund_mgr_lst[i].split('Portfolio Manager')[0].strip()
                # fund_mgr = re.sub(r'.,$','',temp_fund_mgr)
                pos = temp_fund_mgr.rfind(',')
                fund_mgr = temp_fund_mgr[:pos]
                data_dict['fund_manager'] = fund_mgr
                data_dict['fund_manager_years_of_experience_in_industry'] = temp_fund_mgr_exp_list[i].replace(\
                                                                                'Industry Experience Since','').replace(\
                                                                                'Industry Experience since','').strip()
                data_dict['fund_manager_years_of_experience_with_fund']=fund_manager_years_of_experience_with_fund_lst[i].replace('Joined VanEck in','').strip()
            fund_manager_list.append(data_dict)
            
        for i in range(len(items)):
            items[i]['fund_managers'] = fund_manager_list
            
        return  items
