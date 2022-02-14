from gencrawl.items.hospital.hospital_detail_item import HospitalDetailItem
from gencrawl.spiders.hospital.hospital_detail_spider import HospitalDetailSpider
from copy import deepcopy
import re


class AshlandmmcComHospitalDetail(HospitalDetailSpider):
    name = 'hospital_detail_ashlandmmc_com_us'

    def get_items_or_req(self, response, default_item={}):
        items = super().get_items_or_req(response, default_item)
        items = deepcopy(items[0])
        raw_address = response.xpath('//div[contains(@style,"padding:")]').get()

        raw_address_1 = ''.join(re.findall(r'Location:([\s\S]+\d{3}-\d{3}-\d{4})', raw_address))
        raw_address_2 = ''.join(re.findall(r'Clinic:([\s\S]+\d{3}-\d{3}-\d{4} | [\s\S]+\(\d{3}\)\s\d{3}-\d{4})',
                                           raw_address))
        raw_address_3 = ''.join(re.findall
                                (r'<p> <\/p>\n<p> <\/p>\n<p> <\/p>\n<p> <\/p>\n<p> <\/p>\n<p> <\/p>'
                                 r'([\s\S]+)', raw_address))
        raw_address_4 = ''.join(re.findall(r'<h2><\/h2>\n<h2><\/h2>([\s\S]+)', raw_address))

        speciality = ''.join(items['speciality'])

        if raw_address_1:
            items['address_raw'] = raw_address_1.replace(speciality, '')
        elif raw_address_2:
            items['address_raw'] = raw_address_2.replace(speciality, '')
        elif raw_address_3:
            items['address_raw'] = raw_address_3.replace(speciality, '')
        else:
            items['address_raw'] = raw_address_4.replace(speciality, '')

        yield self.generate_item(items, HospitalDetailItem)
