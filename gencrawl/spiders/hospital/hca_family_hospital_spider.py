import os
import scrapy
import csv
from datetime import datetime
from gencrawl.util.statics import Statics
import re
import json
from gencrawl.items.hospital.hospital_detail_item import HospitalDetailItem
from gencrawl.spiders.hospital.hospital_detail_spider import HospitalDetailSpider
from copy import deepcopy

# scrapy crawl hca_family_hospital_spider -a input_file=hca.csv -a client=DHC -a config=hospital_detail_mountainstar_com_us -o hca_output.jl
class HCAHospitalSpider(HospitalDetailSpider):

    name = "hca_family_hospital_spider"
    custom_settings = {
        "SPIDER_MIDDLEWARES": {
            'scrapy.spidermiddlewares.offsite.OffsiteMiddleware': None,
        },
        # disable name parsing in pipelines
    }
    url_key = "search_url"

    def __init__(self, config=None, *args, **kwargs):
        current_dir = os.getcwd()
        self.retry_condition = None
        self.page_size = 100
        filename = kwargs.get("input_file")
        self.input_fp = os.path.join(current_dir, Statics.PROJECT_DIR, Statics.RES_DIR, filename)
        self.logger.info("Input will be fetched from - {}".format(self.input_fp))
        self.post_headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US, en;q=0.9",
            "Access-Control-Allow-Origin": "http://localhost:8065",
            "Content-Type": "application/json"
        }
        self.post_content = {"coids":None,"program":"Web","keyword":None,"zip":None,"latitude":None,"longitude":None,
                             "appointmentTypeId":None,"source":"dotcms","siteType":"Hospital Operations",
                             "startDate":datetime.now().strftime("%Y%m%d"),  "numberDaysOut":549,"gender":None,
                             "languages":None,"meta":{"page":1,"pageSize":self.page_size},"sortType":None,
                             "randomize":True}
        nick_name_rgx = [r'"[a-zA-Z]+"', r'“[a-zA-Z]+”', r'\([a-zA-Z]+\)', r"''[a-zA-Z]+''", r"'[a-zA-Z]+'"]
        self.nick_name_rgx = [re.compile(r) for r in nick_name_rgx]
        super().__init__(config, *args, **kwargs)

    def _get_start_urls(self, urls, input_file, db_limit, prod_only=False):
        objs = []
        with open(self.input_fp) as f:
            csv_reader = csv.DictReader(f)
            for line in csv_reader:
                objs.append(line)
        return objs

    def parse(self, response):
        meta = response.meta
        domain = meta['domain']
        post_url = f"https://{domain}/fadmaa/provider/search/"
        content = deepcopy(self.post_content)
        try:
            content['coids'] = re.search(r'facilityCoids = "(.*?)"', response.text).group(1)
            content['randomizerSeed'] = re.search(r'sessionId = "(.*?)"', response.text).group(1)
        except:
            print("erorrrrrrrrrrrrrrrrrrrr")
        meta['content'] = content
        meta['offset'] = self.page_size
        meta['post_url'] = post_url
        yield scrapy.FormRequest(post_url, method="POST", headers=self.post_headers, body=json.dumps(content),
                                 callback=self.parse_pagination, meta=meta)

    def parse_items(self, response, default_item):
        #https://blakemedicalcenter.com/physicians/profile/Dr-James-DiVincenzo-DPM
        suffix = ['Ill', 'ii', 'lll', 'Ii', 'Sr', 'V', 'JR', 'Iv', 'SR', 'Jr.', 'II', 'Iii', 'II.', 'Sr.', 'VII', 'VI',
                  'Jr', 'III', 'JR.', 'IV', 'SR.']
        suffix = sorted(suffix, key=len, reverse=True)
        for jsn in response:
            item = self.generate_item(deepcopy(default_item), HospitalDetailItem)
            item['website'] = default_item['website']
            item['_profile_id'] = item['gencrawl_id']
            item['npi'] = jsn.get("physicianNpi")
            # if item['npi'] not in temp:
            #     continue
            if item['npi'] and len(item['npi'].strip()) != 10:
                item['npi'] = ''
            item['first_name'] = jsn['physicianFirstName']
            for rgx in self.nick_name_rgx:
                item['first_name'] = re.sub(rgx, '', item['first_name']).strip()

            item['middle_name'] = jsn['physicianMiddleInitial']
            if item['middle_name'] and (" " + item['middle_name']) in item['first_name']:
                item['middle_name'] = ''
            elif item['middle_name']:
                for rgx in self.nick_name_rgx:
                    item['middle_name'] = re.sub(rgx, '', item['middle_name']).strip()
            item['last_name'] = jsn['physicianLastName']
            for rgx in self.nick_name_rgx:
                item['last_name'] = re.sub(rgx, '', item['last_name']).strip()
            item['designation'] = jsn['physicianDesignation']
            item['raw_full_name'] = " ".join(
                [a for a in [item['first_name'], item['middle_name'], item['last_name']] if a])
            if item['designation']:
                item['raw_full_name'] = item['raw_full_name'] + ", " + item['designation']
            last_name = item['last_name'].replace(", ", " ").replace(" ,", " ").replace(",", " ").split(" ")
            if len(last_name) > 1:
                for s in suffix:
                    if s in last_name:
                        last_name = [l for l in last_name if l != s]
                        item['last_name'] = " ".join(last_name).replace(s, '').strip()
                        item['suffix'] = s
                        break

            item['doctor_url'] = "https://{}/physicians/profile/{}".format(item['website'], jsn['urlTitle'])

            if jsn.get("affiliations"):
                item['affiliation'] = [a.get("locationName") for a in jsn['affiliations']]

            if jsn.get("providerSpecialties"):
                item['speciality'] = [a.get("specialty") for a in jsn['providerSpecialties']]
            locations = jsn.get("providerLocations")
            if locations:
                for loc in jsn['providerLocations']:
                    nitem = deepcopy(item)
                    nitem['practice_name'] = loc['name']
                    nitem['city'] = loc['city']
                    nitem['state'] = loc['state']
                    nitem['zip'] = loc['zip']
                    nitem['phone'] = loc['phone']
                    nitem['fax'] = loc['fax']
                    address = loc['street']
                    if address:
                        address_lines = address.rsplit(",", 2)
                        if len(address_lines) == 3:
                            nitem['address_line_1'], nitem['address_line_2'], nitem['address_line_3'] = address_lines
                        elif len(address_lines) == 2:
                            nitem['address_line_1'], nitem['address_line_2'] = address_lines
                        else:
                            nitem['address_line_1'] = address_lines[0]

                        if ' Ste ' in nitem['address_line_1'] and not nitem.get("address_line_2"):
                            add = nitem['address_line_1'].split(" Ste ")
                            nitem['address_line_1'], nitem['address_line_2'] = add[0], "Ste " + add[1]
                    yield nitem
            else:
                yield item

    def parse_pagination(self, response):
        default_item = self.get_default_item(response)
        default_item['website'] = response.meta['domain']
        resp_jsn = json.loads(response.text)
        for item in self.parse_items(resp_jsn['result']['providerList'], default_item):
            yield item

        meta = response.meta
        total_results = meta.get("total_results") or resp_jsn['result']['totalProvidersCount']
        if total_results > meta['offset']:
            content = meta['content']
            content['meta']['page'] += 1
            meta['offset'] = meta['offset'] + self.page_size
            yield scrapy.FormRequest(meta['post_url'], method="POST", headers=self.post_headers, body=json.dumps(content),
                                     callback=self.parse_pagination, meta=meta)
