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

class CommunityhospitalofanacondaOrgHospitalDetail(HospitalDetailSpider):

    name = 'hospital_detail_communityhospitalofanaconda_org_us'
    custom_settings={
    "HTTPCACHE_ENABLED":False
    }

    def get_items_or_req(self, response, default_item={}):

        items = self.prepare_items(response, default_item)
        meta = response.meta
        if items[0]['address_raw']!=[]:
            addresses = items[0]['address_raw']
            addresses = re.split('(\d+)',addresses)
            addresses = ' '.join(addresses)
            addresses = [addresses][0].split('\n \n')
            phone_nos = response.xpath("//h2[@class='feature14 heading doc-office-number']/following-sibling::text()[1]").getall()
            phone_nos = phone_nos[0].split('/')

            for c,address in enumerate(addresses):
                if c>0:
                    item_copy = copy.deepcopy(items[0])
                    items.append(item_copy)
            for c,item in enumerate(items):
                item['address_raw'] = re.split('(\d+)',addresses[c]) # as a list
                item['phone'] = phone_nos[c]
                yield self.generate_item(item, HospitalDetailItem)
        else:
            phone_nos = response.xpath("//h2[@class='feature14 heading doc-office-number']/following-sibling::text()[1]").getall()
            items[0]['phone'] = phone_nos
            practice_name = response.xpath("//h2[contains(text(),'Facility/Office:')]/following-sibling::text()").get()

            if practice_name is not None:
                items[0]['practice_name'] = practice_name

            yield self.generate_item(items[0], HospitalDetailItem)
    