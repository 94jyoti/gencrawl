from gencrawl.items.hospital.hospital_detail_item import HospitalDetailItem
from gencrawl.spiders.hospital.hospital_detail_spider import HospitalDetailSpider
from copy import deepcopy
import re


class GearycommunityhospitalOrgHospitalDetail(HospitalDetailSpider):
    name = 'hospital_detail_gearycommunityhospital_org_us'

    def get_items_or_req(self, response, default_item={}):
        items = super().get_items_or_req(response, default_item)
        items = deepcopy(items[0])
        temp_address = list()
        raw_address = response.xpath('//div[@class="wpb_wrapper"]/h3/following-sibling::p').getall()
        extra_address = response.xpath('//p[contains(.,"This provider practices at:")]/following-sibling::p').getall()
        extra_address_2 = response.xpath('//div[@class="wpb_wrapper"]//p').get()

        if raw_address:
            raw_address = re.split(r'(\d{5})', ''.join(raw_address))
            raw_address = ''.join(raw_address[:2])
            temp_address.append(raw_address)

        if extra_address:
            extra_address = re.split(r'(\d{5})', ''.join(extra_address))
            extra_address = ''.join(extra_address[:2])
            temp_address.append(extra_address)

        if temp_address:
            for address in temp_address:
                items['address_raw'] = address
                yield self.generate_item(items, HospitalDetailItem)
        elif extra_address_2:
            items['address_raw'] = extra_address_2
            yield self.generate_item(items, HospitalDetailItem)
        else:
            yield self.generate_item(items, HospitalDetailItem)