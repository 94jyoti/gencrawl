from gencrawl.items.hospital.hospital_detail_item import HospitalDetailItem
from gencrawl.spiders.hospital.hospital_detail_spider import HospitalDetailSpider
from copy import deepcopy


class HolyCrossMedicalCenter_org_us(HospitalDetailSpider):

    name = 'hospital_detail_holycrossmedicalcenter_org_us'

    def get_items_or_req(self, response, default_item=None):
        items = super().get_items_or_req(response, default_item)
        items = deepcopy(items[0])

        connector_urls = response.xpath("//ul[@id='practices-grid-list']/li/a/@href").getall()

        if not connector_urls:
            yield self.generate_item(items, HospitalDetailItem)

        else:
            for connector_url in connector_urls:
                yield self.make_request(connector_url, callback=self.parse_address_fields, meta={"item": items},
                                        dont_filter=True)

    def parse_address_fields(self, response):
        items = response.meta['item']
        items = deepcopy(items)
        items['practice_name'] = response.xpath("//h1[@class='blockHeader']/text()").get()
        items['address_raw'] = response.xpath("//div[@class='contact-info']").get()

        yield self.generate_item(items, HospitalDetailItem)
