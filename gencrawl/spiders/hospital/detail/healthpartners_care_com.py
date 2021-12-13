from gencrawl.items.hospital.hospital_detail_item import HospitalDetailItem
from gencrawl.spiders.hospital.hospital_detail_spider import HospitalDetailSpider
from copy import deepcopy
from datetime import datetime
import re
from gencrawl.util.statics import Statics

class HealthPartnersCareCom(HospitalDetailSpider):

    name = 'hospital_detail_healthpartners_com_care_us'

    def get_items_or_req(self, response, default_item={}):

        items = self.prepare_items(response, default_item)
        affiliations  = ', '.join(re.findall(r'\{name\:\"(.*?)\,customUrl',response.text)).replace('"','').strip()
        for item in items:
            try:
                item['affiliation'] = affiliations
            except:
                item['affiliation'] = ''
            yield self.generate_item(item, HospitalDetailItem)
