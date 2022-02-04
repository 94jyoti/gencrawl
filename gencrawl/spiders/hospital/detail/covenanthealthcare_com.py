from gencrawl.items.hospital.hospital_detail_item import HospitalDetailItem
from gencrawl.spiders.hospital.hospital_detail_spider import HospitalDetailSpider
from copy import deepcopy
import re


class CovenanthealthcareComHospitalDetail(HospitalDetailSpider):
    name = 'hospital_detail_covenanthealthcare_com_us'

    def get_items_or_req(self, response, default_item={}):
        items = super().get_items_or_req(response, default_item)
        items = deepcopy(items[0])
        raw_address = response.xpath("//div[contains(@class,'physicians-location')]/div").getall()
        for address in raw_address:
            temp_practice = re.search(r'<div class="additional-location-fields">([\s\S]+)<br>', address)
            if temp_practice:
                items['address_raw'] = address
                yield self.generate_item(items, HospitalDetailItem)
            else:
                yield self.generate_item(items, HospitalDetailItem)
# this code is for reusable for purpose to discuss in dev call
                # temp_address.append(address)
                # temp.append(temp_address)
                # print(temp_address[-1])
                # print(temp_address[0])
                # items['address_raw'] = address
                # del temp_address[0]
                # temp_address.pop(0)

        # print(raw_address)
        # if raw_address:
        #     cleaned_add_raw = re.sub(r'<.*?>', ' ', str(raw_address)).strip()
        #     print('+++++++++', cleaned_add_raw)
        #     cleaned_add_raw = ast.literal_eval(cleaned_add_raw)
        #     cleaned_add_raw = [(i.replace('\r', '').replace('\n', '').replace('Hours', '')).strip() for i in cleaned_add_raw]
        #     print(cleaned_add_raw)
        #     for address in cleaned_add_raw:
        #         if address:
        #             items['address_raw'] = address
        #             yield self.generate_item(items, HospitalDetailItem)
        #     print(type(cleaned_add_raw))

            # for i in cleaned_add_raw:
            #     print(i)
            # print(type(cleaned_add_raw))
            # print(cleaned_add_raw)
        #     cleaned_add_raw = cleaned_add_raw.split('Hours')
        #     print(len(cleaned_add_raw))
            # print(type(cleaned_add_raw))
            # for each in cleaned_add_raw:
            #     print('asbd')
            #     print(each)
            # cleaned_add_raw = [address.replace('Hours','') for address in cleaned_add_raw]
            # print(cleaned_add_raw)
