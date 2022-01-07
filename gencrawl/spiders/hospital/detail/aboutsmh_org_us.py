from gencrawl.items.hospital.hospital_detail_item import HospitalDetailItem
from gencrawl.spiders.hospital.hospital_detail_spider import HospitalDetailSpider
from datetime import datetime
from gencrawl.util.statics import Statics


class AboutsmhOrgHospitalDetail(HospitalDetailSpider):

    name = 'hospital_detail_aboutsmh_org_us'

    def get_items_or_req(self, response, default_item=None):
        items = super().get_items_or_req(response, default_item)
        print(len(items))
        if(len(items)==1):
            items[0]['phone']=",".join(response.xpath("//span[contains(@class,'address-block')]/span/parent::span/following-sibling::span[contains(@class,'phone-number-block')]/span/a/text()").extract())
        for item in items:
            yield self.generate_item(item, HospitalDetailItem)