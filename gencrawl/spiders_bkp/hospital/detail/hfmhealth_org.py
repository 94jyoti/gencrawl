from gencrawl.items.hospital.hospital_detail_item import HospitalDetailItem
from gencrawl.spiders.hospital.hospital_detail_spider import HospitalDetailSpider
from copy import deepcopy
import re


class HfmhealthOrgHospitalDetail(HospitalDetailSpider):
    name = 'hospital_detail_hfmhealth_org_us'

    def get_items_or_req(self, response, default_item={}):
        items = super().get_items_or_req(response, default_item)
        items = deepcopy(items[0])
        count = 0
        raw_address = response.xpath('//h4[contains(@class,"Location")]').getall()
        cleaned_address = re.sub('<.*?>', '', ''.join(raw_address))
        if cleaned_address:
            raw_address = re.split(r'(\d{5})', ''.join(raw_address))
            while count < len(raw_address)-1:
                address = raw_address[count:count+2]
                address = (''.join(address)).split('|')
                practice_name = re.sub(r'<.*?>', '   ', address[0]).strip()
                practice_name = re.sub(r'  +', ', ', practice_name).replace('amp;', '')
                # address = (address[1].strip()).replace('<sup>', '').replace('</sup>', '')
                address = re.sub(r'<.*?>', '', address[1]).strip()
                count = count + 2

                items['practice_name'] = practice_name
                items['address_raw'] = address
                yield self.generate_item(items, HospitalDetailItem)

        else:
            yield self.generate_item(items, HospitalDetailItem)
