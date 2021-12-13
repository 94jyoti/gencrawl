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
        print(json_data)
        item['first_name'] = json_data['physicianFirstName']
        item['middle_name'] = json_data['physicianMiddleInitial']
        print("ejsvcsc",item['middle_name'])
        item['last_name'] = json_data['physicianLastName']
        item['designation'] = json_data['physicianDesignation']
        if(item['middle_name'] is None):
            #item['middle_name']=""
            item['raw_full_name'] = item['first_name'] +" "+item['last_name']+", " +item['designation']
        else:
            item['raw_full_name'] = item['first_name'] + " " + item['middle_name']+" "+item['last_name']+ ", " + item['designation']
          #  print("ndkcndk")
        provider_speciality=[]
        item['first_name'] =""
        item['middle_name'] = ""
        #print("ejsvcsc", item['middle_name'])
        item['last_name'] = ""
        for spe in json_data['providerSpecialties']:
            provider_speciality.append(spe['specialty'])
        item['speciality']=",".join(provider_speciality)
        provider_affiliation=[]
        for aff in json_data['affiliations']:
            provider_affiliation.append(aff['locationName'])
        item['affiliation'] = ",".join(provider_affiliation)
        temp_item=[]

        for count,ele in enumerate(json_data['providerLocations']):
            print(ele)
            print(count)
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
            print(temp_item[count])
            yield self.generate_item(temp_item[count], HospitalDetailItem)





'''
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
        #yield self.generate_item(item, HospitalDetailItem)
'''