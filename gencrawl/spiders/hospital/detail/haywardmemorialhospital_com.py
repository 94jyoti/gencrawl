from gencrawl.items.hospital.hospital_detail_item import HospitalDetailItem
from gencrawl.spiders.hospital.hospital_detail_spider import HospitalDetailSpider
from copy import deepcopy


class Haywardmemorialhospital_org_us(HospitalDetailSpider):
    name = 'hospital_detail_haywardmemorialhospital_com_us'

    def get_items_or_req(self, response, default_item=None):
        items = super().get_items_or_req(response, default_item)
        for item in items:
            if (item['raw_full_name'] == []):
                try:
                    item['raw_full_name']=response.xpath("//article[@id='main']//strong/text()[not(contains(.,'Phone'))]").extract()[0]
                except:
                    temp_name = (response.xpath("//h1[contains(text(),'Providers')]/following-sibling::h3/text()").extract()[0]).split(",")
                    try:
                        item['raw_full_name'] = temp_name[1] + " " + temp_name[0] + " " + temp_name[2:]

                    except:
                        item['raw_full_name'] = temp_name[1] + " " + temp_name[0]

        connector_urls = "https://haywardmemorialhospital.com/find-a-provider/"

        yield self.make_request(connector_urls, callback=self.parse_speciality, meta={"item": items}, dont_filter=True)

    def parse_speciality(self, response):
        items = response.meta['item']
        item = items[0]
        #print(item['raw_full_name'])
        temp_raw_name = response.xpath("//div[@id='providerLoop']/div//h2[1]/text()").extract()
        #print(temp_raw_name)
        for name in range(len(temp_raw_name)):
            #print("rawfullnameeeeeee",item['raw_full_name'])
            #print("temp name",temp_raw_name[name])
            #print("dvsvsd",item['raw_full_name'].strip() in temp_raw_name[name].strip())

            if (item['raw_full_name'].strip() in temp_raw_name[name].strip()):
                item['raw_full_name'] = temp_raw_name[name]
                #print("ifififififif")
                item['speciality'] = response.xpath("//div[@id='providerLoop']/div[" + str(name + 1) + "]//following-sibling::p[position()<last()]//text()").extract()
                #print(item['speciality'])
            elif(temp_raw_name[name].strip() in item['raw_full_name'].strip()):
                item['speciality'] = response.xpath("//div[@id='providerLoop']/div[" + str(
                    name + 1) + "]//following-sibling::p[position()<last()]//text()").extract()
        for i in range(len(item['speciality'])):
            item['speciality'][i]=item['speciality'][i].replace("\n","").strip()
        item['raw_full_name']=item['raw_full_name'].replace(",","").replace("Cert.","")

        yield self.generate_item(item, HospitalDetailItem)
