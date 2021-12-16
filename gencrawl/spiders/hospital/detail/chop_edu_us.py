from gencrawl.items.hospital.hospital_detail_item import HospitalDetailItem
from gencrawl.spiders.hospital.hospital_detail_spider import HospitalDetailSpider
from datetime import datetime
from gencrawl.util.statics import Statics

class ChopEduHospitalDetail(HospitalDetailSpider):

    name = 'hospital_detail_chop_edu_us'

    def get_items_or_req(self, response, default_item={}):

        items = self.prepare_items(response, default_item)
        meta = response.meta
        meta['items'] = items
        if(len(response.xpath("//strong[contains(text(),'Location')]/following-sibling::a[1]/@href").extract_first())==0):
            yield self.generate_item(items[0], HospitalDetailItem)
        else:
            address_urls="https://www.chop.edu/"+response.xpath("//strong[contains(text(),'Location')]/following-sibling::a[1]/@href").extract_first()
            print(address_urls)
            yield self.make_request(address_urls, callback=self.parse_information, meta=meta, dont_filter=True)

    def parse_information(self, response):
        meta = response.meta
        items = meta['items']
        for item in items:
            item['practice_name'] = response.xpath("//h1[contains(@class,'node-title')]//text()").extract_first()
            item['address_raw'] = response.xpath("//div[contains(@class,'field-address')]").extract_first()
            item['phone'] = response.xpath("//div[contains(text(),'Contact')]//following-sibling::a//text()").extract_first()
            #item['fax'] = response.xpath("//div[contains(text(),'Fax')]//following-sibling::a//text()").extract_first()
            yield self.generate_item(item, HospitalDetailItem)
