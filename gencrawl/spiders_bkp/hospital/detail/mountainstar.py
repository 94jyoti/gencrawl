from gencrawl.items.hospital.hospital_detail_item import HospitalDetailItem
from gencrawl.spiders.hospital.hospital_detail_spider import HospitalDetailSpider
from copy import deepcopy
import re
import json
from gencrawl.util.statics import Statics

class MountainStarComHospitalDetail(HospitalDetailSpider):

    name = 'hospital_detail_mountainstar_com_us'

    def get_items_or_req(self, response, default_item={}):

        items = self.prepare_items(response, default_item)
        item = items[0]
        meta = response.meta
        meta['items'] = items
        data = re.findall("var physician = (.*?);",response.text)[0]
        json_data = json.loads(data)
        item['first_name'] = json_data['physicianFirstName']
        item['middle_name'] = json_data['physicianMiddleInitial']
        item['last_name'] = json_data['physicianLastName']
        item['designation'] = json_data['physicianDesignation']
        if(item['middle_name'] is None):
            item['raw_full_name'] = item['first_name'] +" "+item['last_name']+", " +item['designation']
        else:
            item['raw_full_name'] = item['first_name'] + " " + item['middle_name']+" "+item['last_name']+ ", " + item['designation']
        provider_speciality=[]
        item['first_name'],item['middle_name'],item['last_name'] = "","",""
        for spe in json_data['providerSpecialties']:
            provider_speciality.append(spe['specialty'])
        item['speciality']=",".join(provider_speciality)
        provider_affiliation=[]
        for aff in json_data['affiliations']:

            provider_affiliation.append(aff['locationName'])

        item['affiliation'] = ",".join(provider_affiliation)
        temp_item=[]

        for count,ele in enumerate(json_data['providerLocations']):

            temp_item.append(deepcopy(item))
            temp_item[count]['zip']=json_data['providerLocations'][count]['zip']
            temp_item[count]['city']=json_data['providerLocations'][count]['city']
            temp_item[count]['state']=json_data['providerLocations'][count]['state']
            temp_item[count]['phone']=json_data['providerLocations'][count]['phone']
            temp_item[count]['fax']=json_data['providerLocations'][count]['fax']
            temp_item[count]['practice_name']=json_data['providerLocations'][count]['name']
            temp_item[count]['address_line_1']=json_data['providerLocations'][count]['street']
            if (temp_item[count]['address_line_1'] == temp_item[count]['city']):
                temp_item[count]['city'] = ""
            temp_item[count]['address_raw'] = temp_item[count]['practice_name'] + " " + temp_item[count]['address_line_1'] + " " + temp_item[count]['city'] + " " + \
                                  temp_item[count]['state'] + " " + temp_item[count]['zip']
            yield self.generate_item(temp_item[count], HospitalDetailItem)
