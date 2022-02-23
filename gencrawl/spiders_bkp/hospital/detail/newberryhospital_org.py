from gencrawl.items.hospital.hospital_detail_item import HospitalDetailItem
from gencrawl.spiders.hospital.hospital_detail_spider import HospitalDetailSpider
from copy import deepcopy
import re


class NewberryhospitalOrgHospitalDetail(HospitalDetailSpider):
    name = 'hospital_detail_newberryhospital_org_us'

    def get_items_or_req(self, response, default_item={}):
        items = super().get_items_or_req(response, default_item)
        items = deepcopy(items[0])
        raw_address_1 = response.xpath('(//h2[contains(text(),"Location")]/following-sibling::text())[1]').getall()
        raw_address_1 = re.sub('\n  +', '', ''.join(raw_address_1))
        raw_address_2 = response.xpath('//h2[contains(.,"Location")]/following-sibling::p').getall()
        raw_address_2 = [text for text in raw_address_2 if text not in '<p>\xa0</p>']

        if raw_address_1:
            items['address_raw'] = raw_address_1.replace('Newberry Office:', '').replace('Chapin Office:', '')
            items['phone'] = response.xpath('//span[@class="phone"]//text()[contains(., "T")]').get()
            items['fax'] = response.xpath('//span[@class="phone"]//text()[contains(., "F")]').get()

            yield self.generate_item(items, HospitalDetailItem)

        if raw_address_2:
            for i, address in enumerate(raw_address_2):
                phone = response.xpath('//span[@class="phone"]//text()[contains(., "T")]').getall()
                items['address_raw'] = address.replace('Newberry Office:', '').replace('Chapin Office:', '')
                items['phone'] = phone[i]
                items['fax'] = response.xpath('//span[@class="phone"]//text()[contains(., "F")]').get()
                yield self.generate_item(items, HospitalDetailItem)

        else:
            yield self.generate_item(items, HospitalDetailItem)