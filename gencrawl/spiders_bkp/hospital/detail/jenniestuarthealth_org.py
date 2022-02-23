from gencrawl.items.hospital.hospital_detail_item import HospitalDetailItem
from gencrawl.spiders.hospital.hospital_detail_spider import HospitalDetailSpider
from copy import deepcopy
import re


class JenniestuarthealthOrgHospitalDetail(HospitalDetailSpider):
    name = "hospital_detail_jenniestuarthealth_org_us"

    def get_items_or_req(self, response, default_item=None):
        items = super().get_items_or_req(response, default_item)
        items = deepcopy(items[0])

        if items.get("address_raw"):
            # speciality = (items['speciality'][0].split(','))[0]
            reg = "^([^,]*)"
            speciality = re.search(reg, ''.join(items['speciality']))
            if speciality:
                speciality = speciality.group(1)
                items['address_raw'] = items['address_raw'].replace(speciality, '')

                yield self.generate_item(items, HospitalDetailItem)

        else:
            yield self.generate_item(items, HospitalDetailItem)


