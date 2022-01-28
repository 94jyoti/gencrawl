from gencrawl.items.hospital.hospital_detail_item import HospitalDetailItem
from gencrawl.spiders.hospital.hospital_detail_spider import HospitalDetailSpider
from copy import deepcopy


class BaconcountyhospitalComHospitalDetail(HospitalDetailSpider):
    name = 'hospital_detail_baconcountyhospital_com_us'

    def get_items_or_req(self, response, default_item=None):
        items = super().get_items_or_req(response, default_item)
        items = deepcopy(items[0])
        address = ''
        address_raw = response.xpath('//h2[contains(text(),"Office:")]/following-sibling::text()[position()>2]').getall()

        for line in address_raw:
            address = address + line + '<br>'
            if line == '\n':
                break
        items['address_raw'] = address.replace(".", ",")

        yield self.generate_item(items, HospitalDetailItem)

