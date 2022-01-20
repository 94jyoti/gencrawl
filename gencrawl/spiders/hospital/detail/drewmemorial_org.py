from gencrawl.items.hospital.hospital_detail_item import HospitalDetailItem
from gencrawl.spiders.hospital.hospital_detail_spider import HospitalDetailSpider
from copy import deepcopy
import re


class DrewMemorialOrgHospitalDetail(HospitalDetailSpider):

    name = 'hospital_detail_drewmemorial_org_us'

    def get_items_or_req(self, response, default_item=None):
        items = super().get_items_or_req(response, default_item)
        items = deepcopy(items[0])

        try:
            cleaned_add_raw = re.sub(r'<.*?>',' ', str(items['address_raw'])).strip()
            address = response.xpath('//p[text()="SeArk Surgical Specialists"]/following-sibling::p').get()
            cleaned_add_raw = cleaned_add_raw.replace('Location of Primary office:', '')

            if not cleaned_add_raw:
                practice_name = response.xpath('//p[text()="Location of Primary office:"]/following-sibling::p[1]').get()
                address_line_1 = response.xpath('//p[text()="Location of Primary office:"]/following-sibling::p[2]').get()
                address_line_2 = response.xpath('//p[text()="Location of Primary office:"]/following-sibling::p[3]').get()
                phone = response.xpath('//p[text()="Location of Primary office:"]/following-sibling::p[4]').get()
                items['practice_name'] = practice_name
                items['address_raw'] = address_line_1+address_line_2
                items['phone'] = phone
                yield self.generate_item(items, HospitalDetailItem)

            elif address:
                items['address_raw'] = address
                yield self.generate_item(items, HospitalDetailItem)

            else:
                yield self.generate_item(items, HospitalDetailItem)

        except:
            yield self.generate_item(items, HospitalDetailItem)

