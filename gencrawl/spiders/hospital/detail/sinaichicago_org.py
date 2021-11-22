from gencrawl.items.hospital.hospital_detail_item import HospitalDetailItem
from gencrawl.spiders.hospital.hospital_detail_spider import HospitalDetailSpider
from copy import deepcopy
from datetime import datetime
import re
from gencrawl.util.statics import Statics

class SinaiChicagoOrg(HospitalDetailSpider):

    name = 'hospital_detail_sinaichicago_org'

    def get_items_or_req(self, response, default_item={}):

        items = self.prepare_items(response, default_item)
        slug = response.url.split('results')[1].replace('/','').strip()
        data_url = 'https://www.sinaichicago.org/en/wp-json/wp/v2/doctors/?slug='+ str(slug)
        meta = response.meta
        meta['items'] = items
        yield self.make_request(data_url, callback=self.parse_locations, meta=meta, dont_filter=True)
    

    def parse_locations(self, response):
        items = response.meta['items']
        try:
            items[0]['affiliation'] = re.findall(r'hospital_affiliations.*?li\>(.*?)<',response.text)[0]
        except:
            items[0]['affiliation'] = ''
        yield self.generate_item(items[0], HospitalDetailItem)