from gencrawl.items.hospital.hospital_detail_item import HospitalDetailItem
from gencrawl.spiders.hospital.hospital_detail_spider import HospitalDetailSpider
import re
from copy import deepcopy


class ScrmcComHospitalDetail(HospitalDetailSpider):

    name = 'hospital_detail_scrmc_com_us'

    def get_items_or_req(self, response, default_item=None):
        items = super().get_items_or_req(response, default_item)
        item = deepcopy(items[0])

        connector_urls = response.xpath('//div[@class="bottom"]//p/a[not(@rel="tag")]/@href').getall()

        if not connector_urls:
            item['practice_name'] = ''

            yield self.generate_item(item, HospitalDetailItem)

        else:
            for connector_url in connector_urls:
                yield self.make_request(connector_url, callback=self.parse_address_fields, meta={"item": items[0]},
                                        dont_filter=True)

    def parse_address_fields(self, response):
        item = response.meta['item']
        item = deepcopy(item)
        doctor_page_phone = item['phone']

        item['address_raw'] = response.xpath('//div[@class="col-xs-12"][2]/p').get()
        item['practice_name'] = response.xpath('//div[contains(@class,"page-body")]//h1/text()').get()
        fax = response.xpath('//h3[contains(text(), "Contact")]/following-sibling::p[1]//text()'
                             '[(contains(., "Fax")) and not(contains(., "info"))]').get()
        item['fax'] = ''.join(re.findall("\\d+-\\d+-\\d+", str(fax)))

        phone = response.xpath('//h3[contains(text(), "Contact")]/following-sibling::p[1]//text()'
                                       '[not(contains(., "Fax")) and not(contains(., "@"))]').get()

        item['phone'] = ''.join(re.findall("\\d+-\\d+-\\d+", str(phone))) or doctor_page_phone

        yield self.generate_item(item, HospitalDetailItem)