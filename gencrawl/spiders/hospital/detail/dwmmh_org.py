from gencrawl.items.hospital.hospital_detail_item import HospitalDetailItem
from gencrawl.spiders.hospital.hospital_detail_spider import HospitalDetailSpider
from copy import deepcopy


class DwmmhOrgHospitalDetail(HospitalDetailSpider):

    name = 'hospital_detail_dwmmh_org_us'

    def get_items_or_req(self, response, default_item=None):
        items = super().get_items_or_req(response, default_item)
        items = deepcopy(items[0])

        address = response.xpath("(//text()[preceding-sibling::h2[1][text()='Facility/Office:']])").getall()
        address = [i for i in address if i != '\n']
        if len(address) == 1 and any(char.isdigit() for char in address[0]):
            items['practice_name'] = ''
            items['address_raw'] = ''.join(address)
        else:
            items['address_raw'] = ' <br>'.join(address)

        yield self.generate_item(items, HospitalDetailItem)






