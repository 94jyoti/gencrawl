from gencrawl.items.hospital.hospital_detail_item import HospitalDetailItem
from gencrawl.spiders.hospital.hospital_detail_spider import HospitalDetailSpider
from copy import deepcopy
import re


class HighlandsHospitalOrg(HospitalDetailSpider):
    name = 'hospital_detail_highlandshospital_org_us'

    def get_items_or_req(self, response, default_item={}):
        items = super().get_items_or_req(response, default_item)
        items = deepcopy(items[0])
        phone = response.xpath("//p[contains(text(),'For more help')]/preceding-sibling::p[1]//text()").extract()
        if phone:
            phone_num = phone[-1].replace('\n','').strip()
        items['phone'] = phone_num
        zip = items['address'].split()[-1]
        if re.findall(r'\d\d\d\d\d',zip):
            items['zip'] = zip
            items['state'] = items['address'].split()[-2]
        else:
            items['zip'] = ''
            items['city'] = zip
        yield self.generate_item(items, HospitalDetailItem)
