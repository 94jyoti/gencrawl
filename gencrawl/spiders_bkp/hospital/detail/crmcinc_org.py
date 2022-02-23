from gencrawl.items.hospital.hospital_detail_item import HospitalDetailItem
from gencrawl.spiders.hospital.hospital_detail_spider import HospitalDetailSpider
from copy import deepcopy
import re


class CrmcincOrgHospitalDetail(HospitalDetailSpider):
    name = "hospital_detail_crmcinc_org_us"

    def get_items_or_req(self, response, default_item=None):
        items = super().get_items_or_req(response, default_item)
        items = deepcopy(items[0])
        address_raw = items.get('address_raw')

        if items.get("address_raw"):
            address_raw = items.get('address_raw')
            practice_name = re.search(r'^(\D*\w\D*)', address_raw)
            practice_name = practice_name.group(1)
            if practice_name[-1].isdigit():
                practice_name = practice_name.replace(practice_name[-1], '')
            address_raw = address_raw.replace(practice_name, '')
            practice_name = practice_name.replace('Practice(s)', '')
            items['address_raw'] = address_raw
            items['practice_name'] = practice_name

            yield self.generate_item(items, HospitalDetailItem)

        else:
            address_raw = address_raw.replace('Practice(s)', '')
            items['address_raw'] = address_raw

            yield self.generate_item(items, HospitalDetailItem)