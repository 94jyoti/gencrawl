from gencrawl.items.hospital.hospital_detail_item import HospitalDetailItem
from gencrawl.spiders.hospital.hospital_detail_spider import HospitalDetailSpider
from copy import deepcopy
from datetime import datetime
import re
from gencrawl.util.statics import Statics

class CvphOrg(HospitalDetailSpider):

    name = 'hospital_detail_cvph_org_us'

    def get_items_or_req(self, response, default_item={}):
        items = self.prepare_items(response, default_item)
        meta = response.meta
        meta['items'] = items
        practice_names = response.xpath("//div[div[dl[@id='provider-address']]]//dl[@id='provider-address']/parent::div/parent::div/parent::div//div[h4]/h4/text()").extract()
        for i in range(len(items)):
            try:
                items[i]['practice_name'] = practice_names[i]
                
            except:
                items[i]['practice_name'] = ''
            yield self.generate_item(items[i], HospitalDetailItem)

    
    
    