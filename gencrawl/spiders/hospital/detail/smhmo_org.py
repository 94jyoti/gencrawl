from gencrawl.items.hospital.hospital_detail_item import HospitalDetailItem
from gencrawl.spiders.hospital.hospital_detail_spider import HospitalDetailSpider
from copy import deepcopy
import re


class SmhmoOrgHospitalDetail(HospitalDetailSpider):
    name = 'hospital_detail_smhmo_org_us'

    def get_items_or_req(self, response, default_item={}):
        items = super().get_items_or_req(response, default_item)
        items = deepcopy(items[0])
        raw_address = response.xpath('(//div[@class="infobox"])[3]').get()
        practice_1 = response.xpath('(//div[@class="infobox"])[3]/p[1]/text()').get()
        practice_2 = response.xpath('(//div[@class="infobox"])[3]/p[2]/text()').get()
        practice_match_1 = re.search(r'(\D+)\d', str(practice_2))

        if practice_match_1:
            practice_2 = practice_match_1.group(1)
            raw_address = raw_address.replace(practice_2, '').replace(practice_1, '')
            practice_name = practice_1 + ',' + practice_2

        elif practice_2 and not any(char.isdigit() for char in practice_2):
            raw_address = raw_address.replace(practice_2, '').replace(practice_1, '')
            practice_name = practice_1 + ',' + practice_2

        else:
            raw_address = raw_address.replace(practice_1, '')
            practice_name = practice_1

        items['practice_name'] = practice_name
        items['address_raw'] = raw_address
        yield self.generate_item(items, HospitalDetailItem)
