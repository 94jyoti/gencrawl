from gencrawl.items.hospital.hospital_detail_item import HospitalDetailItem
from gencrawl.spiders.hospital.hospital_detail_spider import HospitalDetailSpider
from copy import deepcopy
from datetime import datetime
import re
from gencrawl.util.statics import Statics

class BonseCoursComUS(HospitalDetailSpider):

    name = 'hospital_detail_bonsecours_com_us'

    def get_items_or_req(self, response, default_item={}):
        items = self.prepare_items(response, default_item)
        meta = response.meta
        meta['items'] = items
        phone_block = response.xpath("//div[@id='react-locations']/@data-locations").extract()[0]
        phone_list = re.findall(r'\"Phone\"\:\"(.*?)\"',phone_block)
        for i in range(len(items)):
            try:
                items[i]['phone'] = phone_list[i]
            except:
                try:
                    gen_phone_num = response.xpath("//img[contains(@src,'phone')]/following-sibling::a[1]/text()").extract()[0]
                    items[i]['phone'] = gen_phone_num
                except:
                    items[i]['phone'] = ''
            yield self.generate_item(items[i], HospitalDetailItem)

    
    
    