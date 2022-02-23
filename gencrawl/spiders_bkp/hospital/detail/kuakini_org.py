from gencrawl.items.hospital.hospital_detail_item import HospitalDetailItem
from gencrawl.spiders.hospital.hospital_detail_spider import HospitalDetailSpider
from datetime import datetime
from gencrawl.util.statics import Statics
import scrapy
import json
import copy
from bs4 import BeautifulSoup
import re


class KuakiniOrgHospitalDetail(HospitalDetailSpider):
    name = 'hospital_detail_kuakini_org_us'

    def parse(self, response):
        items = self.prepare_items(response, default_item=self.get_default_item(response))
        data = re.findall(r'({id.*);data_list\.push\(item\)',response.text)
        for d in data:
            d = d.replace("'",'').replace('"','').replace('/',' ')
            raw_full_name = re.findall(r'toLowerCase\(\)\,name:(.*)\,specialty', d)
            item_copy = copy.deepcopy(items[0])
            item_copy['doctor_url'] = ''
            item_copy['raw_full_name'] = ' '.join(raw_full_name[0].split(',')[:-1])
            item_copy['designation'] = raw_full_name[0].split(',')[-1]
            item_copy['speciality'] = re.findall(r"specialty:(\b[A-Za-z,\s]+\b)", d)
            item_copy['address_raw'] = re.findall(r"location:(.*),phone1", d)[0]
            item_copy['phone'] = re.findall(r"phone1:(.*),affiliation", d)[0]
            item_copy['affiliation'] = [a.replace('KuakiniPublic Physician Affiliation','').strip() for a in re.findall(r"affiliation: (\b[A-Za-z,\s]+\b)", d)]
            yield self.generate_item(item_copy, HospitalDetailItem)