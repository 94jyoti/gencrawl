from gencrawl.items.hospital.hospital_detail_item import HospitalDetailItem
from gencrawl.spiders.hospital.hospital_detail_spider import HospitalDetailSpider
from copy import deepcopy


class MrhmeOrgHospitalDetail(HospitalDetailSpider):
    name = 'hospital_detail_mrhme_org_us'

    def get_items_or_req(self, response, default_item=None):
        items = super().get_items_or_req(response, default_item)
        temp_item=items[0]
        items=[]
        temp_raw_name=response.xpath("//h2[@class='box_header']/text()").extract()

        temp_data=response.xpath("//div[@class='details_box']")
        for row in temp_data:
            items = deepcopy(temp_item)

            items['raw_full_name'] =row.xpath(".//h2//text()").extract()[0]
            items['speciality'] = row.xpath(".//ul[@class='info_list clearfix']//label[contains(text(),'Special')]/following-sibling::div/text()").extract()[0]
            items['address_raw']=" ".join(row.xpath(".//ul[@class='info_list clearfix']//label[contains(text(),'Contact Info')]/following::div[1]/text()[position()>1]").extract())
            try:
                items['phone'] = row.xpath(".//ul[@class='info_list clearfix']//label[contains(text(),'Contact Info')]/following::div[1]/text()[position()=1]").extract()[0]
            except:
                pass
            #print("dvd", items['phone'])
            #
            
            yield self.generate_item(items, HospitalDetailItem)

            #print(items['raw_full_name'])

'''

        for item in range(len(temp_raw_name)):
            items=deepcopy(temp_item)



            items['raw_full_name']=temp_raw_name[item]
            items['speciality']=response.xpath("(//label[contains(text(),'Special')])["+str(item+1)+"]/following-sibling::div/text()").extract()
            items['address_raw']=" ".join(response.xpath("(//ul[@class='info_list clearfix']/li//label[contains(text(),'Contact Info')])["+str(item+1)+"]/following-sibling::div//text()[position()>1]").extract())
            #xfor i in items
            print("address",items['address_raw'])
            items['phone']=response.xpath("(//label[contains(text(),'Contact Info')])["+str(item+1)+"]/following-sibling::div/text()[1]").extract()
            yield self.generate_item(items, HospitalDetailItem)
'''