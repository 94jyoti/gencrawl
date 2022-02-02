from gencrawl.items.hospital.hospital_detail_item import HospitalDetailItem
from gencrawl.spiders.hospital.hospital_detail_spider import HospitalDetailSpider
from copy import deepcopy
import re

class OlympicmedicalOrgHospitalDetail(HospitalDetailSpider):

    name = 'hospital_detail_olympicmedical_org_us'

    def get_items_or_req(self, response, default_item={}):
        items = super().get_items_or_req(response, default_item)
        items = deepcopy(items[0])

        raw_address = response.xpath('//div[@id="ProviderTabContent3"]').getall()
        if raw_address:
            cleaned_add_raw = re.sub(r'<.*?>', ' ', "".join(raw_address)).strip()
            cleaned_add_raw = cleaned_add_raw.split('Directions &amp; More')
            # might need to use
            # addresses = re.findall(r'([\d\D]+)Directions &amp; More', cleaned_add_raw)
            for address in cleaned_add_raw:
                if address:
                    items['address_raw'] = address.replace("amp;", "")
                    yield self.generate_item(items, HospitalDetailItem)