from gencrawl.items.hospital.hospital_detail_item import HospitalDetailItem
from gencrawl.spiders.hospital.hospital_detail_spider import HospitalDetailSpider
from copy import deepcopy
from datetime import datetime
import re
from gencrawl.util.statics import Statics
import scrapy
import json
import copy
from scrapy.selector import Selector

class CalverthealthmedicineOrgHospitalDetail(HospitalDetailSpider):

    name = 'hospital_detail_calverthealthmedicine_org_us'
    custom_settings={
    "HTTPCACHE_ENABLED":False
    }

    def get_items_or_req(self, response, default_item={}):

        items = self.prepare_items(response, default_item)
        meta = response.meta
        raw_text = response.xpath("//div[@class='info']//text()").getall()
        address_1 = list(filter(lambda v: re.match('^\d+.*[a-z]+.*[A-Z]+.*', v), raw_text))
        practice_names = []
        fax_nos = []
        phone_nos =[]
        address_2_list = []
        for t in address_1:
            practice_name = response.xpath("//*[contains(text(),'"+t+"')]/preceding-sibling::li[1]/label/text()").get()
            practice_names.append(practice_name)
            address_2 = response.xpath("//*[contains(text(),'"+t+"')]/following-sibling::text()[1]").get()
            address_2_list.append(address_2)
            phone = response.xpath("(//*[contains(text(),'"+t+"')]/following-sibling::li/label[contains(text(),'P:')])[1]/../text()").get()
            phone_nos.append(phone)
            fax = response.xpath("(//*[contains(text(),'"+t+"')]/following-sibling::li/label[contains(text(),'F:')])[1]/../text()").get()
            fax_nos.append(fax)

        if len(address_1)>1:
            item_copy = copy.deepcopy(items[0])
            items.append(item_copy)
        
        for c,item in enumerate(items):
            item['practice_name'] = practice_names[c]
            item['phone'] = phone_nos[c]
            item['fax'] = fax_nos[c]
            item['address_raw'] = [address_1[c]+"\n"+ address_2_list[c]]
            
            yield self.generate_item(item, HospitalDetailItem)
