import requests
import csv
from io import BytesIO
import io
import codecs
import json
import os
import pandas as pd
import numpy as np
from gencrawl.util.statics import Statics
from gencrawl.util.utility import Utility
from gencrawl.settings import CONFIG_DIR, SPIDER_DIR
from gencrawl.settings import CLIENT as DEFAULT_CLIENT
SPIDER_TEMPLATE = '''from gencrawl.spiders.financial.financial_detail_spider import FinancialDetailSpider
from gencrawl.spiders.financial.financial_detail_field_mapping import FinancialDetailFieldMapSpider
from gencrawl.spiders.hospital.hospital_detail_spider import HospitalDetailSpider
import scrapy


class {spider_cls}({parent_cls}):
    name = '{domain}_detail_{website}'

    def get_items_or_req(self, response, default_item=None):
        items = super().get_items_or_req(response, default_item)
        return items
'''


class GoogleConfig:

    def __init__(self, client=None):
        self.spider = None
        self.config_name = None
        self.client = client or DEFAULT_CLIENT
        if self.client == Statics.CLIENT_DHC:
            self.google_link = "https://docs.google.com/spreadsheets/u/1/d/1jnhZlAxHDAfBXoy6kZu9SQsdsNY-BarKx4G7t2wy7aw/export?format=csv&id=1jnhZlAxHDAfBXoy6kZu9SQsdsNY-BarKx4G7t2wy7aw&gid=1934331278"
        else:
            self.google_link = "https://docs.google.com/spreadsheets/u/1/d/1jnhZlAxHDAfBXoy6kZu9SQsdsNY-BarKx4G7t2wy7aw/export?format=csv&id=1jnhZlAxHDAfBXoy6kZu9SQsdsNY-BarKx4G7t2wy7aw&gid=1108971848"
        self.spider_class_map = {"financial_detail": "FinancialDetailSpider",
                                 "financial_detail_field_map": "FinancialDetailFieldMapSpider",
                                 "hospital_detail": "HospitalDetailSpider"}

    def download_csv_file(self, url):
        response = requests.get(url)
        df = pd.read_csv(io.StringIO(response.content.decode('utf-8')))
        return df

    def filter_website_in_config(self, df, website):
        df = df.set_index('field_names', drop=True).T
        df1 = df.copy()
        df = df.reset_index()
        website_df = df[df['Config'] == website]
        if not website_df.empty:
            website_index = website_df.index[0]
            website_df = df1[website_index: website_index+4]
            do_fresh_copy = website_df.pop('Refresh Copy')[0]
            if do_fresh_copy != '1':
                print("Refresh Copy set to 0, so exiting without saving configuration....")
                return pd.DataFrame()

        return website_df

    def create_configs(self, df):
        def split_g(elem):
            if isinstance(elem, float):
                return []
            elems = elem.replace("\r\n", "\n").replace("\r", "\n").split("\n")
            elems = [e for e in elems if e and e.strip()]
            return elems

        parsed_config_list = dict()
        parsed_config = dict()
        website = df.pop('Config')[0]
        parsed_config['website'] = website
        self.spider = df.pop('Spider')[0]
        domain = self.spider.split("_")[0]
        crawl_type = self.spider.split("_")[1]
        parsed_config['domain'] = domain
        parsed_config['crawl_method'] = Statics.CRAWL_METHOD_DEFAULT
        parsed_config['allowed_domains'] = Utility.get_allowed_domains([website])
        if 'allowed_domains' in df.keys():
            parsed_config['allowed_domains'].extend(split_g(df.pop("allowed_domains")[0]))

        parsed_config['parsing_type'] = Statics.PARSING_TYPE_DEFAULT
        parsed_config['country'] = "US"
        parsed_config['language'] = "ENGLISH"

        parsed_config[crawl_type] = dict()
        detail = parsed_config[crawl_type]
        detail['spider'] = self.spider
        detail["crawl_method"] = df.pop("Crawl Method")[0]
        # if detail['crawl_method'] == Statics.CRAWL_METHOD_SELENIUM:
        #     detail['wait_time'] = Statics.WAIT_TIME_DEFAULT
        #     detail['custom_settings'] = {
        #       "HTTPCACHE_ENABLED": False
        #     }
        detail["parsing_type"] = Statics.PARSING_TYPE_XPATH
        detail['start_urls'] = split_g(df.pop("fund_urls")[0])
        if 'custom_settings' in df.keys():
            custom_settings = split_g(df.pop('custom_settings')[0])
            if custom_settings:
                custom_settings = json.loads(custom_settings[0])
                detail["custom_settings"] = custom_settings

        if 'decision_tags' in df.keys():
            decision_tags = split_g(df.pop('decision_tags')[0])
            if decision_tags:
                decision_tags = json.loads(decision_tags[0])
                parsed_config["decision_tags"] = decision_tags

        ext_codes = dict()
        detail["ext_codes"] = ext_codes
        xpaths = dict()
        cleanups = dict()
        return_types = dict()
        selectors = dict()
        for index in range(0, 4):
            if index == 0:
                obj = xpaths
            elif index == 1:
                obj = cleanups
            elif index == 2:
                obj = return_types
            elif index == 3:
                obj = selectors
            for field, value in df.iloc[index].iteritems():
                obj[field] = None if np.nan is value else value

        for field in xpaths:
            ext_code = dict()
            if xpaths.get(field):
                ext_codes[field] = ext_code
                ext_code["paths"] = split_g(xpaths[field])
            if cleanups.get(field) and np.nan is not cleanups[field]:
                if split_g(cleanups[field]):
                    ext_code["cleanup_functions"] = split_g(cleanups[field])

            rt = return_types.get(field)
            s = selectors.get(field)

            if field.startswith("temp_"):
                rt = 'selector'
                ext_code['child_return_strategy'] = s or Statics.RETURN_STRATEGY_DEFAULT
                s = None

            ext_code['return_type'] = rt or Statics.RETURN_TYPE_DEFAULT
            ext_code['selector'] = s or Statics.SELECTOR_ROOT

        crawl_type_config = parsed_config.get(crawl_type)
        if crawl_type_config:
            codes = crawl_type_config.get("ext_codes") or {}
            pagination = codes.pop("pagination", None)
            if pagination:
                crawl_type_config['pagination'] = {"pagination": pagination}

        file_name = Utility.get_config_name(website)
        parsed_config_list[file_name] = parsed_config
        self.config_name = file_name
        return parsed_config_list

    def create_custom_script(self, configs):
        spider = self.spider
        domain = spider.split("_")[0]
        crawl_type = spider.split("_")[1]
        for config_name, jsn in configs.items():
            jsn[crawl_type]['spider'] = spider
            spider_fp = os.path.join(SPIDER_DIR, domain, crawl_type, config_name + ".py")
            if not os.path.exists(spider_fp):
                with open(spider_fp, 'w') as w:
                    spider_cls = config_name.split("_")
                    spider_cls.append(crawl_type)
                    spider_cls = [c[0].upper() + c[1:].lower() for c in spider_cls]
                    spider_cls = ''.join(spider_cls)
                    parent_cls = self.spider_class_map[spider.replace("_custom_spider", "")]
                    template = SPIDER_TEMPLATE.format(domain=spider.split("_")[0], spider_cls=spider_cls,
                                                      parent_cls=parent_cls, website=config_name)
                    w.write(template)

    def save_configs(self, configs, config_dir):
        for filename, jsn in configs.items():
            filename = filename + Statics.CONFIG_EXT
            fp = os.path.join(config_dir, filename)
            print(fp)
            with open(fp, 'w') as w:
                w.write(json.dumps(jsn, indent=4))

    def main(self, website, config_dir, env):
        df = self.download_csv_file(self.google_link)
        website_df = self.filter_website_in_config(df, website)
        if not website_df.empty:
            p_configs = self.create_configs(website_df)
            # only write files in development env

            if env == Statics.ENV_DEV:
                if self.spider.endswith("_custom_spider"):
                    self.create_custom_script(p_configs)

                self.save_configs(p_configs, config_dir)
            return p_configs[list(p_configs.keys())[0]]
        else:
            print("No matched website- {} configuration found on google sheet.......".format(website))


