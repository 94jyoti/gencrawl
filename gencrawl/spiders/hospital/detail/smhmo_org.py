from gencrawl.items.hospital.hospital_detail_item import HospitalDetailItem
from gencrawl.spiders.hospital.hospital_detail_spider import HospitalDetailSpider
from copy import deepcopy
import re


class SmhmoOrgHospitalDetail(HospitalDetailSpider):
    name = 'hospital_detail_smhmo_org_us'

    def get_items_or_req(self, response, default_item={}):
        items = super().get_items_or_req(response, default_item)
        items = deepcopy(items[0])
        raw_address = response.xpath('(//div[@class="infobox"])[3]').getall()
        for address in raw_address:
            if address:
                # ^(.* ?)\d
                practice_match = re.search(r'^([\s\S]+?)\d', address)
                if practice_match:
                    practice_name = practice_match.group(1)
                    address = address.replace(practice_name, '')
                    practice_name = re.sub(r'<.*?>', '', practice_name).strip()
                    practice_name = practice_name.replace('\r', '')
                    practice_name = re.sub(' +', ' ', practice_name)
                    practice_name = ','.join(practice_name.split('\n'))
                    items['practice_name'] = practice_name
                    items['address_raw'] = address
                    yield self.generate_item(items, HospitalDetailItem)

            else:
                yield self.generate_item(items, HospitalDetailItem)
