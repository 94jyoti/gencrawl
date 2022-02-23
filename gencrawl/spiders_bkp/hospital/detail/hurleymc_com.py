from gencrawl.items.hospital.hospital_detail_item import HospitalDetailItem
from gencrawl.spiders.hospital.hospital_detail_spider import HospitalDetailSpider
from copy import deepcopy
from datetime import datetime
import re
from gencrawl.util.statics import Statics

class HurleyMcCom(HospitalDetailSpider):

    name = 'hospital_detail_hurleymc_com_us'

    def get_items_or_req(self, response, default_item={}):
        items = self.prepare_items(response, default_item)
        meta = response.meta
        meta['items'] = items
        for i in range(len(items)):
            # import pdb;pdb.set_trace() needs discussion as framework not supporting 6 digit zip
            try:
                items[i]['zip'] = re.findall(r'(\s+\d+)\<\/div.*?office\-contact',items[i]['address_raw'])[0].strip()
            except:
                items[i]['zip'] = ''
            yield self.generate_item(items[i], HospitalDetailItem)

    
    
    