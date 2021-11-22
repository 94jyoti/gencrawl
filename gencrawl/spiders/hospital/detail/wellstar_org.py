from requests.sessions import cookiejar_from_dict
from gencrawl.items.hospital.hospital_detail_item import HospitalDetailItem
from gencrawl.spiders.hospital.hospital_detail_spider import HospitalDetailSpider
from copy import deepcopy
from datetime import datetime
import re
from gencrawl.util.statics import Statics
import requests

# scrapy crawl hospital_detail  -a config="hospital_detail_northernlighthealth_org_us" -a client=DHC -o "north1.csv"
# https://prod.d17wl9oyb3enor.amplifyapp.com/
class WellStarOrg(HospitalDetailSpider):

    name = "hospital_detail_wellstar_org_us"
    
    def get_items_or_req(self, response, default_item={}):
        import pdb;pdb.set_trace()
        items = self.prepare_items(response, default_item)
        cookie_token = "hZ_L9yQtcyvF6HRc6OC6yeAZjU0M4DYA95kDkAVKDB4Z-sknIQPxvrVer7gN0WF0DW6r438teAzhAS1VSIPviDNz50plmXMdkkEYvT1RPlY1;"
        physician_id = response.xpath("//input[@id='physicianItemID']/@value").extract()[0]
        verification_token = response.xpath("//input[contains(@name, '__RequestVerificationToken')]/@value").extract()[0]
        headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'Connection': 'keep-alive',
            '__RequestVerificationToken': verification_token,
            'Cookie': '__RequestVerificationToken={}'.format(cookie_token),
            'User-Agent': 'My User Agent 1.0',
            'Accept': '*/*'
        }
        url = "https://www.wellstar.org/api/PhysicianDetailApi/PhysicianLocations"
        data = {"searchTerm":physician_id}
        import json
        
        resp = requests.post(url, json=data, headers=headers, allow_redirects=False)
        fax_url = resp.text
        # data = searchTerm: "{1BFCC215-A183-46E8-9296-C607FD50DA27}"}
        # url = LocationDetails

        # slug = response.url.split("results")[1].replace("/","").strip()
        # data_url = "https://www.sinaichicago.org/en/wp-json/wp/v2/doctors/?slug="+ str(slug)
        meta = response.meta
        meta["items"] = items
        yield self.generate_item(items[0], HospitalDetailItem)
        # yield self.make_request(items[0]['doctor_url'], callback=self.parse_locations, meta=response.meta, dont_filter=True, method=Statics.CRAWL_METHOD_SELENIUM)

        #yield self.make_request(data_url, callback=self.parse_locations, meta=meta, dont_filter=True)

    def parse_locations(self, response):
        items = response.meta["items"]
        cookie_token = "hZ_L9yQtcyvF6HRc6OC6yeAZjU0M4DYA95kDkAVKDB4Z-sknIQPxvrVer7gN0WF0DW6r438teAzhAS1VSIPviDNz50plmXMdkkEYvT1RPlY1;"
        physician_id = response.xpath("//input[@id='physicianItemID']/@value").extract()[0]
        verification_token = response.xpath("//input[contains(@name, '__RequestVerificationToken')]/@value").extract()[0]
        headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'Connection': 'keep-alive',
            '__RequestVerificationToken': verification_token,
            'Cookie': '__RequestVerificationToken={}'.format(cookie_token),
            'User-Agent': 'My User Agent 1.0',
            'Accept': '*/*'
        }
        url = "https://www.wellstar.org/api/PhysicianDetailApi/PhysicianLocations"
        data = {"searchTerm":physician_id}
        import json
        # import ipdb;ipdb.set_trace()
        resp = requests.post(url, json=data, headers=headers, allow_redirects=False)
        fax_url = resp.text
        # try:
        #     items[0]["affiliation"] = re.findall(r"hospital_affiliations.*?li\>(.*?)<",response.text)[0]
        # except:
        #     items[0]["affiliation"] = ""
        yield self.generate_item(items[0], HospitalDetailItem)