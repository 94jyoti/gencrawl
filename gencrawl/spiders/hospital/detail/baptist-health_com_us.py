from gencrawl.items.hospital.hospital_detail_item import HospitalDetailItem
from gencrawl.spiders.hospital.hospital_detail_spider import HospitalDetailSpider
from copy import deepcopy
from datetime import datetime
import re
from gencrawl.util.statics import Statics
import scrapy
import json


class BaptistHealthHospitalDetail(HospitalDetailSpider):

    name = 'hospital_detail_baptist-health_com_us'

    def get_items_or_req(self, response, default_item=None):
        items = super().get_items_or_req(response, default_item)
        items = deepcopy(items[0])

        connector_urls = response.xpath('//a[@class="doctor-other-location-link"]//@href').getall()


        if not connector_urls:
            yield self.generate_item(items, HospitalDetailItem)

        else:
            flag=1
            #connector_urls.insert(1, "1")
            if (flag == 1):
                yield self.generate_item(items, HospitalDetailItem)
                flag = 0

            for connector_url in connector_urls:


                #items.append(deepcopy(items[0]))
                yield self.make_request(connector_url, callback=self.parse_address_fields, meta={"item": items},
                                        dont_filter=True)

    def parse_address_fields(self, response):
        items = response.meta['item']
        items = deepcopy(items)
        #items['address_raw']=""
        items['practice_name']=response.xpath("(//h1)[1]//text()").extract()[0]
        items['phone']=""
        items['fax']=""
        items['address_raw'] = response.xpath('//p[contains(@class,"elementor-icon-box-description")]').get()
        yield self.generate_item(items, HospitalDetailItem)