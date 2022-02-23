from gencrawl.items.hospital.hospital_detail_item import HospitalDetailItem
from gencrawl.spiders.hospital.hospital_detail_spider import HospitalDetailSpider
from copy import deepcopy
from datetime import datetime
import re
from gencrawl.util.statics import Statics

class UrmcRochesterEdu(HospitalDetailSpider):

    name = 'hospital_detail_urmc_rochester_edu_us'

    def get_items_or_req(self, response, default_item={}):
        items = self.prepare_items(response, default_item)
        meta = response.meta
        meta['items'] = items
        practice_names = response.xpath("//h3[contains(text(),'Locations')]/following-sibling::div/p/a/span[1]/text()").extract()
        for i in range(len(items)):
            try:
                prct = practice_names[i]
                invalid_prct = re.findall(r'^\d+',prct)
                if invalid_prct:
                    items[i]['practice_name'] = ''
                else:
                    items[i]['practice_name'] = practice_names[i]
            except:
                items[i]['practice_name'] = ''
            yield self.generate_item(items[i], HospitalDetailItem)

    
    
    