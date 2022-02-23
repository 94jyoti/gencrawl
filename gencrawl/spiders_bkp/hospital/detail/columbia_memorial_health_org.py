from gencrawl.items.hospital.hospital_detail_item import HospitalDetailItem
from gencrawl.spiders.hospital.hospital_detail_spider import HospitalDetailSpider
from copy import deepcopy
from datetime import datetime
import re
from gencrawl.util.statics import Statics

class ColumbiaMemorialHealthOrg(HospitalDetailSpider):

    name = 'hospital_detail_columbiamemorialhealth_org_us'

    def get_items_or_req(self, response, default_item={}):
        items = self.prepare_items(response, default_item)
        meta = response.meta
        meta['items'] = items
        
        speciality = response.xpath("//p[contains(text(),'Specialty')]/text()[1]").extract()
        if speciality:
            items[0]['speciality'] = speciality[0].replace('Specialty:','').strip()
        else:
            items[0]['speciality'] = ''
        
        affiliation_text = ' '.join(response.xpath("//p[contains(text(),'Specialty')]//text()").extract())
        if 'Affiliation' in affiliation_text:
            temp_affiliation = affiliation_text.split('Affiliation')[1]\
                .replace('(s)','').replace(':','')
            if '\n' in temp_affiliation:
                affiliation = temp_affiliation.split('\n')[0].strip()
            else:
                affiliation = temp_affiliation
            items[0]['affiliation'] = affiliation
        else:
            items[0]['affiliation'] = ''

        yield self.generate_item(items[0], HospitalDetailItem)

    
    
    