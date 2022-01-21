from gencrawl.items.hospital.hospital_detail_item import HospitalDetailItem
from gencrawl.spiders.hospital.hospital_detail_spider import HospitalDetailSpider
from copy import deepcopy
import re


class SelfRegionalOrgHospitalDetail(HospitalDetailSpider):
    name = 'hospital_detail_selfregional_org_us'

    def get_items_or_req(self, response, default_item=None):
        items = super().get_items_or_req(response, default_item)
        items = deepcopy(items[0])

        try:
            address_raw = response.xpath('//div[@class="physician-office"]').get()
            check_pass = re.match(r"<div class='physician-office'>([\S\n\t\v ]+)</div>", address_raw)
            addresses = address_raw.split('</iframe>')
            for address in addresses:
                if address == '\t\t\t\t</div>':
                    break
                else:
                    phone = re.findall(r'\(\d*\)\s\d*\-\s\d*', address)
                    if phone:
                        phone = (''.join(phone)).replace('- ', '-')
                        print(phone)
                        address = address.replace(phone,'')
                        items['phone'] = phone
                        items['address_raw'] = address

                        yield self.generate_item(items, HospitalDetailItem)
                    else:
                        items['address_raw'] = ''.join(address)
                        yield self.generate_item(items, HospitalDetailItem)



            # if check_pass:
            #     address = address_raw.split('</div>', 1)
            #     print('dvfb',address)
            # cleaned_add_raw = re.sub(r'<.*?>', ' ', address_raw).strip()
            # if cleaned_add_raw:
            #     addresses = re.split(r'\s{3}', cleaned_add_raw)
            #     print('fghb',addresses)
            #     # items['address_raw'] = address_raw
            #     # for address in addresses:
            #     #     items['address_raw'] = address
            #     #     yield self.generate_item(items, HospitalDetailItem)
            #
            # else:
            #     yield self.generate_item(items, HospitalDetailItem)

        except:
            yield self.generate_item(items, HospitalDetailItem)
