from gencrawl.items.hospital.hospital_detail_item import HospitalDetailItem
from gencrawl.spiders.hospital.hospital_detail_spider import HospitalDetailSpider
from copy import deepcopy


class Dalemedicalcenter_org_us(HospitalDetailSpider):
    name = 'hospital_detail_dalemedicalcenter_com_us'

    def get_items_or_req(self, response, default_item=None):
        items = super().get_items_or_req(response, default_item)
        for item in items:
            if (item['address_raw'] == []):

                print("xfefef")
                item['address_raw']=response.xpath("//text()[preceding-sibling::h2= 'Facility/Office:']").extract()
            if("University" in item['address_raw']):
                item['address_raw']=item['address_raw'].split("University")[0]



            yield self.generate_item(item, HospitalDetailItem)
