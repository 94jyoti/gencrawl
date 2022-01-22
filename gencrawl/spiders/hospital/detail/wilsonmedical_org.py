from gencrawl.items.hospital.hospital_detail_item import HospitalDetailItem
from gencrawl.spiders.hospital.hospital_detail_spider import HospitalDetailSpider
from copy import deepcopy
import re


class WilsonMedicalOrgHospitalDetail(HospitalDetailSpider):
    name = 'hospital_detail_wilsonmedical_org_us'

    def get_items_or_req(self, response, default_item=None):
        items = super().get_items_or_req(response, default_item)
        items = deepcopy(items[0])

        address_raw = response.xpath('//div[contains(@class,"doc-bio-page")]').get()
        raw_address_1 = re.findall(r'Facility\/Office:([\s\S]*)More\/Other Information:', address_raw)
        raw_address_2 = re.findall(r'Facility\/Office:([\s\S]*)', address_raw)
        phone = response.xpath('//h2[text()="Office:"]/following-sibling::a').get()
        keyword_1 = "Main Office:"
        keyword_2 = "Satellite Office:"
        if raw_address_1:
            raw_address_1 = ''.join(raw_address_1)
            if keyword_1 in raw_address_1:
                addresses = raw_address_1.split(keyword_1)
                for address in addresses:
                    address = address.replace(phone, '')
                    items['address_raw'] = address
                    items['phone'] = phone
                    yield self.generate_item(items, HospitalDetailItem)
            else:
                raw_address_1 = ''.join(raw_address_1)
                addresses = raw_address_1.split(keyword_2)
                for address in addresses:
                    address = address.replace(phone, '')
                    items['address_raw'] = address
                    items['phone'] = phone
                    yield self.generate_item(items, HospitalDetailItem)

        else:
            address = ''.join(raw_address_2)
            address = address.replace(phone, '')
            items['address_raw'] = address
            items['phone'] = phone
            yield self.generate_item(items, HospitalDetailItem)


        


