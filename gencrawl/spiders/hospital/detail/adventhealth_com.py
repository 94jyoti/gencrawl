from gencrawl.items.hospital.hospital_detail_item import HospitalDetailItem
from gencrawl.spiders.hospital.hospital_detail_spider import HospitalDetailSpider
from copy import deepcopy
from datetime import datetime
import re
from gencrawl.util.statics import Statics

class AdventhealthcomhospitalDetail(HospitalDetailSpider):

    name = 'hospital_detail_adventhealth_com'

    def get_items_or_req(self, response, default_item={}):

        items = self.prepare_items(response, default_item)
        fax_block=response.xpath("//div[@class='geolocation']//@data-content").extract()
        print(fax_block)
        fax_list=[]
        for block in fax_block:
            temp_data=re.findall('{"content".*?location-block__fax-text(.*?)location-block__map.*?"}',block.replace("\n",""))
            print(temp_data)
            fax_list.append(re.findall("\d+-\d+-\d+",temp_data[0])[0])
        print(fax_list)
        for i,item in enumerate(items):
            item['fax']=fax_list[i]
            yield self.generate_item(item, HospitalDetailItem)
    