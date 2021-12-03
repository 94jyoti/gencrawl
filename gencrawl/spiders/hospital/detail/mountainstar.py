from gencrawl.items.hospital.hospital_detail_item import HospitalDetailItem
from gencrawl.spiders.hospital.hospital_detail_spider import HospitalDetailSpider
from copy import deepcopy
from datetime import datetime
import re
import json
from gencrawl.util.statics import Statics

class MountainStarhospitalDetail(HospitalDetailSpider):

    name = 'hospital_detail_mountainstar_com'

    def get_items_or_req(self, response, default_item={}):

        items = self.prepare_items(response, default_item)
        item = items[0]
        meta = response.meta
        meta['items'] = items
        file=open("mountainstar.html","w")
        file.write(response.text)
        file.close()
        data = re.findall("var physician = (.*?);",response.text)[0]
        json_data = json.loads(data)
        item['first_name'] = json_data['physicianFirstName']
        item['middle_name'] = json_data['physicianMiddleInitial']
        item['last_name'] = json_data['physicianLastName']
        item['designation'] = json_data['physicianDesignation']
        if(item['middle_name'] is None):
            item['raw_full_name'] = item['first_name'] +" "+item['last_name']+", " +item['designation']
        else:
            item['raw_full_name'] = item['first_name'] + " " + item['middle_name']+" "+item['last_name']+ ",rapy cra " + item['designation']
        provider_speciality=[]
        for spe in json_data['providerSpecialties']:
            provider_speciality.append(spe['specialty'])
        item['speciality']=",".join(provider_speciality)
        provider_affiliation=[]
        for aff in json_data['affiliations']:
            provider_affiliation.append(aff['locationName'])
        item['affiliation'] = ",".join(provider_affiliation)
        item['zip']=json_data['displayLocation']['zip']
        item['city'] = json_data['displayLocation']['city']
        item['state'] = json_data['displayLocation']['state']
        item['phone'] = json_data['displayLocation']['phone']
        item['fax'] = json_data['displayLocation']['fax']
        item['practice_name'] = json_data['displayLocation']['name']
        item['address_line_1'] = json_data['displayLocation']['street']
        if(item['address_line_1']==item['city']):
            item['city']=""
        item['address_raw'] = item['practice_name']+" "+item['address_line_1'] +" " +item['city']+ " "+item['state']+" "+ item['zip']
        yield self.generate_item(item, HospitalDetailItem)