from gencrawl.items.hospital.hospital_detail_item import HospitalDetailItem
from gencrawl.spiders.hospital.hospital_detail_spider import HospitalDetailSpider
from copy import deepcopy


class ArheartComHospitalDetail(HospitalDetailSpider):

    name = 'hospital_detail_arheart_com_us'

    def get_items_or_req(self, response, default_item=None):
        items = super().get_items_or_req(response, default_item)
        items = deepcopy(items[0])

        connector_urls = response.xpath('//li[@class="location"]/a/@href').getall()

        if not connector_urls:

            yield self.generate_item(items, HospitalDetailItem)

        else:
            for connector_url in connector_urls:
                yield self.make_request(connector_url, callback=self.parse_address_fields, meta={"item": items[0]},
                                        dont_filter=True)

    def parse_address_fields(self, response):
        item = response.meta['item']
        item = deepcopy(item)
        item['address_raw'] = response.xpath('//aside[@id="secondary"]//div[contains(@class,"location")]').get()

        yield self.generate_item(item, HospitalDetailItem)
