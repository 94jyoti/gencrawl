from gencrawl.items.hospital.hospital_detail_item import HospitalDetailItem
from gencrawl.spiders.hospital.hospital_detail_spider import HospitalDetailSpider
from copy import deepcopy
from datetime import datetime
import re
from gencrawl.util.statics import Statics


class Excela_Health_Org_us(HospitalDetailSpider):
    name = 'hospital_detail_excelahealth_org_us'

    def get_items_or_req(self, response, default_item={}):
        items = self.prepare_items(response, default_item)
        for item in items:
            try:
                item['address_raw']=item['address_raw'].replace(response.xpath("//section[contains(@id,'Locations')]//ul//span[contains(text(),'Primary Care')]").extract()[0],'')
            except:
                pass
            #item['address_raw'] = item['address_raw'].replace(", <br>", ",")
            yield self.generate_item(item, HospitalDetailItem)