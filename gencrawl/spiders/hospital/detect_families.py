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


class FamilyDetectorSpider(HospitalDetailSpider):

    name = "hospital_detail_auto_family_triaging"
    custom_settings = {
        "ITEM_PIPELINES": {
            'gencrawl.pipelines.validation_pipeline.ValidationPipeline': None,
            'gencrawl.pipelines.dupefilter_pipeline.DupeFilterPipeline': None,
            'gencrawl.pipelines.db_pipeline.DBPipeline': 500
        }
    }

    def __init__(self, config, *args, **kwargs):
        super().__init__(config, *args, **kwargs)
        self.all_configs = []
        self.pipeline = DHCPipeline()

    def get_all_configs_from_db(self):
        engine = create_engine(
            f'postgresql+psycopg2://{GENCRAWL_DB_USER}:{GENCRAWL_DB_PASS}@{GENCRAWL_DB_HOST}:{GENCRAWL_DB_PORT}/{GENCRAWL_DB_NAME}',
            pool_use_lifo=True, pool_pre_ping=True, pool_recycle=3600)
        pg_session = sessionmaker(bind=engine)()
        query = "SELECT config, children, parent FROM public.websites where domain='hospital'"
        print(query)
        results = [{"config": x[0], "children": x[1], "parent": x[2]} for x in pg_session.execute(query)]
        pg_session.close()
        return results

    def get_all_websites(self):
        url = "https://docs.google.com/spreadsheets/u/1/d/1zOeT2OZ4lroqy7Ukt59iaaStxjsl3aYeADenbdii07o/export?format=csv&id=1zOeT2OZ4lroqy7Ukt59iaaStxjsl3aYeADenbdii07o&gid=486472030"
        all_websites = {}
        for row in Utility.read_csv_from_response(requests.get(url)):
            website = row['Website']
            doctor_url = row['qpkey']
            if doctor_url:
                all_websites[website] = doctor_url
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

        for website, doctor_url in all_websites.items():
            config = f"financial_detail_{Utility.get_config_name(website)}_us"
            if config in all_config_names:
                continue

            meta = {"website": website, "doctor_url": doctor_url, "config": config}
            yield self.make_request(doctor_url, callback=self.parse, method=Statics.CRAWL_METHOD_SELENIUM,
                                    meta=meta, dont_filter=True)

    def parse(self, response):
        meta = response.meta
        website = meta['website']
        doctor_url = meta['doctor_url']

        for config in self.all_configs:
            self.config = config
            self.allowed_domains = config['allowed_domains']
            self.website = config['website']
            self.parsing_type = self.config.get('parsing_type') or config['parsing_type']
            self.default_parsing_type = self.config.get("parsing_type") or config.get('parsing_type')
            self.ext_codes = self.config['ext_codes']
            self.retry_condition = self.ext_codes.pop("retry_condition", None)
            self.pipeline.open_spider(self)

            item = self.get_items_or_req(response, default_item=None)[0]
            if item.get("address_raw"):
                item = self.pipeline.process_item(item, self)
                to_yield = False
                for key in ['city', 'state', 'zip']:
                    if item.get(key):
                        to_yield = True
                        break
                if to_yield:
                    nitem = dict(deepcopy(item))
                    nitem['website'] = website
                    nitem['doctor_url'] = doctor_url
                    nitem['gencrawl_id'] = config['pg_id']
                    nitem['address_raw'] = ''
                    yield nitem






