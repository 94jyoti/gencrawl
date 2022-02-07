from gencrawl.items.hospital.hospital_detail_item import HospitalDetailItem
from gencrawl.spiders.hospital.hospital_detail_spider import HospitalDetailSpider
from copy import deepcopy
import re


class TrigghospitalOrgHospitalDetail(HospitalDetailSpider):
    name = 'hospital_detail_trigghospital_org_us'

    def get_items_or_req(self, response, default_item={}):
        items = super().get_items_or_req(response, default_item)
        items = deepcopy(items[0])
        raw_address = response.xpath('//h2[contains(text(),"Facility/Office:")]/following-sibling::text()').getall()
        raw_address = ''.join(raw_address)
        addresses = re.findall(r'([\s\S]+?\d{5})', raw_address)
        print(addresses)
        for address in addresses:
            if address:
                practice_name = re.search(r'([^\d]*)', address)
                if practice_name:
                    practice_name = practice_name.group(1)
                    items['practice_name'] = practice_name.replace('*', '')
                    items['address_raw'] = address.replace(practice_name, '')
                else:
                    items['address_raw'] = address
            yield self.generate_item(items, HospitalDetailItem)


        # print()

        # match = re.search(r'([\s\S]+)(?:Education:)', raw_address)
        # print(re.findall(r'([\s\S]+)(?:Education:)',s))

        # match = re.search(r'([\s\S]+)E[a-z]+:',s)
        # ([\s\S]+\d{5})([\s\S]+\d{5})?

        # if match:
        #     text = match.group(1)
        # # print(text)
        # for address in text.split('\n\n'):
        #     if address:
        #         print(address)
        #
        # items['address_raw'] = raw_address
        # yield self.generate_item(items, HospitalDetailItem)
