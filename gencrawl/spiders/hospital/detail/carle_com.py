import json
import scrapy
from gencrawl.items.hospital.hospital_detail_item import HospitalDetailItem
from gencrawl.spiders.hospital.hospital_detail_spider import HospitalDetailSpider
from copy import deepcopy
from datetime import datetime
import datetime
import urllib.parse
import re
from gencrawl.util.statics import Statics

class CarlecomhospitalDetail(HospitalDetailSpider):
    name = 'carle_com'

    def get_items_or_req(self, response, default_item={}):
        items = self.prepare_items(response, default_item)
        print(items)
        meta = response.meta
        meta['items'] = items
        if(len(response.xpath("//strong[contains(text(),'Other Locations')]/following::a[1]/@href").extract())!=0):
            url="https://carle.org"+response.xpath("//strong[contains(text(),'Other Locations')]/following::a[1]/@href").extract()[0]
            final_url="https://us-nc-paas-cfh-fapapiprod.azurewebsites.net/Location/"+url.split("/")[-1]
            yield self.make_request(final_url, callback=self.parse_locations, meta=meta, dont_filter=True)
        else:
            yield self.generate_item(items[0], HospitalDetailItem)

    def parse_locations(self, response):
        items = response.meta['items']
        item=items[0]
        temp_items=[]
        temp_items.append(deepcopy(item))
        temp_items.append(deepcopy(item))
        print("-------------------------------------------")
        file=open("carle.html","w")
        file.write(response.text)
        file.close()
        #print(response.text)

        temp_items[-1]['address_line_1']=re.findall("<LocationDto.*?<Address1>(.*?)</Address1>.*?</LocationDto>",response.text)[0]
        temp_items[-1]['phone']=re.findall("<LocationDto.*?<Phone>(.*?)</Phone>.*?</LocationDto>",response.text)[0]
        temp_items[-1]['zip']=re.findall("<LocationDto.*?<Zip>(.*?)</Zip>.*?</LocationDto>",response.text)[0]
        temp_items[-1]['city']=re.findall("<LocationDto.*?<City>(.*?)</City>.*?</LocationDto>",response.text)[0]
        temp_items[-1]['state']=re.findall("<LocationDto.*?<State>(.*?)</State>.*?</LocationDto>",response.text)[0]
        for i in temp_items:
            yield self.generate_item(i, HospitalDetailItem)




        #json_data=json.loads(response.text)


'''
        no_of_items=len(response.xpath("//p[@class='location-info']//span[@class='city']//text()").extract()[0])
        temp_items=[]
        for i in range(no_of_items+1):
            temp_items.append(deepcopy(item))

        for item in range(len(temp_items)):
            if(item==0):
                continue
            temp_items[item]['address_raw']=response.xpath("//p[@class='location-info']").extract()

        for i in temp_items:
            yield self.generate_item(i, HospitalDetailItem)








'''




