import os
os.system('export PYTHONPATH="/Users/sagararora/Documents/forage/gencrawl"')
from gencrawl.settings import GENCRAWL_DB_USER, GENCRAWL_DB_PASS, GENCRAWL_DB_HOST, GENCRAWL_DB_PORT, GENCRAWL_DB_NAME
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from gencrawl.util.statics import Statics
from psycopg2.extras import execute_values
from psycopg2 import sql
from gencrawl.util.utility import Utility
import json
import logging
from copy import deepcopy
from gencrawl.spiders.hospital.hospital_detail_spider import HospitalDetailSpider
from gencrawl.pipelines.dhc_pipeline import DHCPipeline
import requests
from urllib.parse import urlparse


"""
This spider will automatically detect websites that follow the same structure.
It extract one page and apply all the configs to that.
To run - scrapy crawl auto_family_triaging -a config=hospital_detail_abc_com_us -o auto_triaging.jl
"""


class FamilyDetectorSpider(HospitalDetailSpider):

    name = "auto_family_triaging"
    custom_settings = {
        "ITEM_PIPELINES": {
            'gencrawl.pipelines.validation_pipeline.ValidationPipeline': None,
            'gencrawl.pipelines.dupefilter_pipeline.DupeFilterPipeline': None,
            'gencrawl.pipelines.db_pipeline.DBPipeline': None
        },
        "DOWNLOAD_DELAY": .5,
        "CONCURRENT_REQUESTS": 32,
        "CONCURRENT_REQUESTS_PER_DOMAIN":  8
    }

    def __init__(self, config, *args, **kwargs):
        super().__init__(config, *args, **kwargs)
        self.all_configs = []
        self.domain = config['pg_id'].split("_")[0]
        self.crawl_type = config['pg_id'].split("_")[1]
        self.country = config['pg_id'].split("_")[-1]
        self.input_url = kwargs.get("input_url") or "https://docs.google.com/spreadsheets/u/1/d/1zOeT2OZ4lroqy7Ukt59iaaStxjsl3aYeADenbdii07o/export?format=csv&id=1zOeT2OZ4lroqy7Ukt59iaaStxjsl3aYeADenbdii07o&gid=486472030"
        # TODO make this dynamic
        self.pipeline = DHCPipeline()
        self.max_length_to_parse = 1000
        self.fields_must = ["address_raw", "raw_full_name"]
        self.fields_any = ['city']

    def get_all_configs_from_db(self):
        engine = create_engine(
            f'postgresql+psycopg2://{GENCRAWL_DB_USER}:{GENCRAWL_DB_PASS}@{GENCRAWL_DB_HOST}:{GENCRAWL_DB_PORT}/{GENCRAWL_DB_NAME}',
            pool_use_lifo=True, pool_pre_ping=True, pool_recycle=3600)
        pg_session = sessionmaker(bind=engine)()
        query = f"""SELECT config, children, parent FROM public.websites 
        WHERE domain='{self.domain}' AND crawl_type='{self.crawl_type}'"""
        print(query)
        results = [{"config": x[0], "children": x[1], "parent": x[2]} for x in pg_session.execute(query)]
        pg_session.close()
        return results

    def get_all_websites(self):
        all_websites = {}
        for row in Utility.read_csv_from_response(requests.get(self.input_url)):
            website = row['Website']
            doctor_url = row['Doctor URL']
            _cached_link = row['Cached URL']
            if doctor_url:
                all_websites[website] = {"doctor_url": doctor_url, "_cached_link": _cached_link}
        self.logger.info("Total websites fetched - {}".format(len(all_websites)))
        return all_websites

    def start_requests(self):
        all_websites = self.get_all_websites()
        db_rows = self.get_all_configs_from_db()
        all_config_names = []
        self.logger.info("Total configs fetched - {}".format(len(db_rows)))
        for row in db_rows:
            config = row['config']
            config_name = config['pg_id']
            all_config_names.append(config_name)
            parent = row['parent']
            if not parent:
                self.all_configs.append(config)

        auto_file = {}
        for line in open("auto_triaging.jl"):
            line = json.loads(line)
            auto_file[line['website']] = 1
        print(len(auto_file))

        for website, url_dict in all_websites.items():
            doctor_url = url_dict['doctor_url']
            _cached_link = url_dict['_cached_link']
            config = f"{self.domain}_{self.crawl_type}_{Utility.get_config_name(website)}_{self.country}"
            if config in all_config_names:
                continue

            if website in auto_file:
                print("continuijg")
                continue

            parsed_url = urlparse(doctor_url)
            home_url = parsed_url.scheme + "://" + parsed_url.netloc
            meta = {"website": website, "doctor_url": doctor_url, "home_url": home_url, "_cached_link": _cached_link}
            yield self.make_request(doctor_url, callback=self.parse_website, method=Statics.CRAWL_METHOD_SELENIUM,
                                    meta=meta, dont_filter=True)

    def parse_website(self, response):
        meta = response.meta
        website = meta['website']
        doctor_url = meta['doctor_url']
        home_url = meta['home_url']
        match_found = False
        for config in self.all_configs:
            # initialization needed to run extraction
            self.config = config
            self.allowed_domains = config['allowed_domains']
            self.website = config['website']
            self.parsing_type = self.config.get('parsing_type') or config['parsing_type']
            self.default_parsing_type = self.config.get("parsing_type") or config.get('parsing_type')
            self.ext_codes = self.config['ext_codes']
            self.retry_condition = self.ext_codes.pop("retry_condition", None)
            self.pipeline.open_spider(self)
            items = self.get_items_or_req(response, default_item=None)
            parsed_items = []
            to_yield = False
            for item in items:
                must_fields_present = True
                for k in self.fields_must:
                    if not item.get(k):
                        must_fields_present = False

                if must_fields_present:
                    if len(str(item)) <= self.max_length_to_parse:
                        parsed_item = self.pipeline.process_item(item, self)
                        parsed_items.append(parsed_item)
                        for key in self.fields_any:
                            if item.get(key):
                                to_yield = True
                                match_found = True
                                break
            if to_yield:
                for item in parsed_items:
                    nitem = dict(deepcopy(item))
                    nitem['website'] = website
                    nitem['config'] = home_url
                    nitem['doctor_url'] = doctor_url
                    nitem['parent_config'] = config['pg_id']
                    nitem['_cached_link'] = response.meta['_cached_link']
                    nitem['address_raw'] = ''
                    nitem['address_raw_1'] = ''
                    yield nitem

        if not match_found:
            item = dict()
            item['website'] = website
            item['config'] = home_url
            item['doctor_url'] = doctor_url
            item['parent_config'] = "NO PARENT FOUND"
            item['_cached_link'] = response.meta['_cached_link']
            yield item








