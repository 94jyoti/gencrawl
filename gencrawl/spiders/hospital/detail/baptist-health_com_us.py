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

    def get_items_or_req(self, response, default_item={}):

        items = self.prepare_items(response, default_item)
        meta = response.meta
        meta['items'] = items
        address_urls=response.xpath("")

        url = "https://service-prep.tenethealth.com/api/Physician/FindPhysician?id=" + physician_id + "&culture=en"

        yield scrapy.Request(url, callback=self.parse_information, meta=meta, dont_filter=True)

    def parse_information(self, response):
        meta = response.meta
        items = meta['items']
        open('aa.html', 'w', encoding='utf-8').write(response.text)
        loaded_json = json.loads(response.text)
        for item in items:
            addresses_block = loaded_json['Addresses']
            for address in addresses_block:
                # print("yyy:",address)
                item['practice_name'] = address['Group']
                item['first_name'] = loaded_json['FirstName']
                item['middle_name'] = loaded_json['MiddleInitial']
                # item['middle_name'] = ""
                # print("ddd:",loaded_json['FirstName'])
                item['last_name'] = loaded_json['LastName']
                item['designation'] = loaded_json['Title']
                item['raw_full_name'] = item['first_name'] + " " + item['middle_name'] + " " + item[
                    'last_name'] + ", " + item['designation']
                item['npi'] = loaded_json['NationalProviderId']
                item['address_line_1'] = address['Address1']
                item['address_line_2'] = address['Address2']
                item['address_line_3'] = ""
                item['city'] = address['City']
                item['state'] = address['State']
                item['zip'] = address['Zip']
                item['phone'] = address['Phone']
                item['fax'] = address['Fax']

                item['speciality'] = [i['Name'] for i in loaded_json['Specialties']]
                item['affiliation'] = [i['Name'] for i in loaded_json['Affiliations']]
                # print("xxx:",item)
                yield self.generate_item(item, HospitalDetailItem)
