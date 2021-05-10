from scrapy import Spider, Request
from jsonpath_ng import jsonpath, parse
from gencrawl.util.statics import Statics
from scrapy.http.response.text import TextResponse
import json
import os
import re
from copy import deepcopy
from datetime import datetime
from scrapy.utils.project import get_project_settings
from gencrawl.util.utility import Utility
from urllib.parse import urlparse, parse_qs
import sys
import logging
import time
import uuid
from gencrawl.settings import DOWNLOADER_MIDDLEWARES, SELENIUM_PATH
from shutil import which
from gencrawl.middlewares.selenium_request import GenSeleniumRequest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from collections import defaultdict
from scrapy.http import HtmlResponse
from collections.abc import Iterable
# logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))


class BaseSpider(Spider):

    @classmethod
    def from_crawler(cls, crawler, config, *args, **kwargs):
        assert config
        config_filename = config + Statics.CONFIG_EXT
        config_fp = os.path.dirname(os.path.realpath(__file__)).split("spiders")[0]
        config_fp = os.path.join(config_fp, Statics.SITE_CONFIG_DIR, config_filename)
        config = json.loads(open(config_fp).read())
        crawl_method = config[cls.crawl_type].get("crawl_method") or config['crawl_method']
        settings_update = {}
        if crawl_method == Statics.CRAWL_METHOD_SELENIUM:
            settings_update['DOWNLOADER_MIDDLEWARES'] = {
                **DOWNLOADER_MIDDLEWARES,
                'gencrawl.middlewares.selenium_request.GenSeleniumMiddleware': 800
            }
            # for chrome driver
            settings_update['SELENIUM_DRIVER_NAME'] = Statics.CHROME_SELENIUM_DRIVER
            settings_update['SELENIUM_DRIVER_EXECUTABLE_PATH'] = SELENIUM_PATH
            settings_update['SELENIUM_DRIVER_ARGUMENTS'] = ['--headless --start-maximized'] #'--headless'
        if settings_update:
            crawler.settings.frozen = False
            crawler.settings.update(settings_update)
            crawler.settings.freeze()
        return super().from_crawler(crawler, config, *args, **kwargs)

    def __init__(self, config, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.settings = get_project_settings()
        urls = kwargs.get("urls")
        if urls:
            urls = urls.split(",")
        self.input_urls = urls
        self.input_file = None
        self.job_id = uuid.uuid1().hex
        self.config = config
        self.specific_config = config[self.crawl_type]
        self.allowed_domains = config['allowed_domains']
        self.website = config['website']
        self.parsing_type = self.specific_config.get('parsing_type') or config['parsing_type']
        self.crawl_method = self.specific_config.get("crawl_method") or config['crawl_method']
        self.wait_time = self.specific_config.get("wait_time") or config.get('wait_time')
        self.default_parsing_type = self.specific_config.get("parsing_type") or config.get('parsing_type')
        self.navigation = self.specific_config.get("navigation")
        # TODO remove this check
        self.navigation = {}
        self.pagination = self.specific_config.get("pagination")
        self.ext_codes = self.specific_config['ext_codes']
        self.default_return_type = Statics.RETURN_TYPE_DEFAULT
        self.default_selector = Statics.SELECTOR_DEFAULT
        self.ignore_fields = ['download_timeout', 'dont_proxy', 'download_slot', 'download_latency', 'depth', 'driver',
                              'selector']

    def _get_start_urls(self):
        input_objs = []
        if self.input_file:
            for line in open(self.input_file):
                url = re.search(r'.*?(http.*)', line)
                if url:
                    # obj = {self.url_key: line.strip()} if line.startswith("http") else json.loads(line)
                    obj = {self.url_key: url.group(1).strip()}
                    input_objs.append(obj)

        if self.input_urls:
            for url in self.input_urls:
                input_objs.append({"url": url})
        self.logger.info("Total urls to be crawled - {}".format(len(input_objs)))
        return input_objs

    def make_request(self, url, callback=None, method=Statics.CRAWL_METHOD_DEFAULT, headers={}, meta={}, body=None,
                     wait_time=Statics.WAIT_TIME_DEFAULT, wait_until=None, iframe=None):
        if method == Statics.CRAWL_METHOD_SELENIUM:
            request = GenSeleniumRequest(url=url, callback=callback, meta=meta, wait_time=wait_time,
                                         wait_until=wait_until, iframe=iframe)
        else:
            if method == Statics.CRAWL_METHOD_GET:
                request = Request(url, callback=callback, meta=meta, headers=headers)
            elif method == Statics.CRAWL_METHOD_POST:
                request = Request(url, callback=callback, method="POST", meta=meta, headers=headers, body=body)
            else:
                self.logger.error(f"Request type is not supported - {method}")
        return request

    def start_requests(self):
        for obj in self._get_start_urls():
            url = obj['url']
            obj['selector'] = Statics.SELECTOR_ROOT
            yield self.make_request(url, callback=self.parse, method=self.crawl_method, meta=obj,
                                    wait_time=self.wait_time, wait_until=self.specific_config.get('wait_until'),
                                    iframe=self.specific_config.get("iframe"))

    def get_default_item(self, response):
        default_item = {}
        for key in response.meta.keys():
            default_item[key] = response.meta[key]
        default_item["job_id"] = self.job_id
        default_item['http_status'] = response.status
        default_item['crawl_datetime'] = datetime.now()
        return default_item

    def parse(self, response):
        default_item = self.get_default_item(response)
        items_or_req = self.get_items_or_req(response, default_item=default_item)
        navigation = self.parse_navigation(response, items_or_req)
        if isinstance(navigation, Iterable):
            yield from navigation
        else:
            yield navigation

    def parse_navigation(self, response, item):
        navigation = self.navigation
        if navigation:
            if navigation[0].get("action") != "follow":
                while navigation:
                    nav = navigation.pop(0)
                    driver = response.meta['driver']
                    xpath = nav.get("ext_codes", {}).get("nav_path")['paths'][0]
                    if nav['action'] == 'click':
                        wait_time = nav['wait_time']
                        if wait_time:
                            if nav.get("wait_until"):
                                WebDriverWait(driver, wait_time).until(
                                    EC.presence_of_element_located((By.XPATH, nav['wait_until']))
                                )
                            else:
                                time.sleep(wait_time)
                        driver.find_element_by_xpath(xpath).click()
                        iframe = nav.get("iframe")
                        if iframe:
                            try:
                                iframe = driver.find_element_by_xpath(iframe)
                                if iframe:
                                    self.driver.switch_to.frame(iframe)
                            except:
                                self.logger.warning(f"iframe not found - {iframe}")
                        response.meta['selector'] = nav['$id']
                        response = response.replace(body=str.encode(driver.page_source))
                        item = self.prepare_items(response, default_item=item)[0]
        return item

    def get_meta(self, meta):
        meta = {k: v for k, v in meta.items() if k not in self.ignore_meta_keys}
        return meta

    def iterate_exec_codes(self, selector_name, selector, ext_codes):
        obj = dict()
        selectors = dict()
        codes = {c: v for c, v in ext_codes.items() if v.get("selector", self.default_selector) == selector_name}
        for key in self._get_ordered_ext_keys(codes):
            jsn = codes[key]
            parsing_type = jsn.get('parsing_type') or self.default_parsing_type
            return_type = jsn.get("return_type") or self.default_return_type
            paths = codes.get(key).get('paths')
            if parsing_type == Statics.PARSING_TYPE_XPATH:
                value = self.apply_xpath(selector, paths, return_type=return_type)
            elif parsing_type == Statics.PARSING_TYPE_JPATH:
                value = self.apply_jpath(selector, paths)
            elif parsing_type == Statics.PARSING_TYPE_REGEX:
                value = self.apply_regex(selector, paths)
            else:
                self.logger.error(f"Unknown parsing type - {parsing_type}")
            value = self.return_value(value, return_type)
            obj[key] = value
            clean_ups = ext_codes.get(key).get('cleanup_functions')
            if clean_ups:
                obj[key] = self.apply_cleanup_func(clean_ups, key, obj)
            if return_type in [Statics.RETURN_TYPE_SELECTOR, Statics.RETURN_TYPE_SELECTOR_JSON]:
                selectors[key] = obj[key]
        return obj, selectors

    def get_mix_items(self, main_obj, selectors, selector_values, ext_codes):
        items = []
        if selectors:
            for selector_name, values in selector_values.items():
                main_obj[selector_name] = str(values)

            for selector_name, values in selector_values.items():
                return_strategy = ext_codes[selector_name].get(
                    "child_return_strategy") or Statics.RETURN_STRATEGY_DEFAULT
                if return_strategy == Statics.RETURN_STRATEGY_SINGLE_ITEM:
                    for value in values:
                        main_obj.update(value)
                    items.append(main_obj)
                elif return_strategy == Statics.RETURN_STRATEGY_SINGLE_OBJECT:
                    main_obj[selector_name.replace(Statics.TEMP_FIELD_PREFIX, "")] = values[0] if values else None
                    items.append(main_obj)
                elif return_strategy == Statics.RETURN_STRATEGY_MULTIPLE_OBJECTS:
                    main_obj[selector_name.replace(Statics.TEMP_FIELD_PREFIX, "")] = values
                    items.append(main_obj)
                elif return_strategy == Statics.RETURN_STRATEGY_MULTIPLE_ITEMS:
                    for value in values:
                        item = deepcopy(main_obj)
                        item.update(value)
                        items.append(item)
                else:
                    self.logger.error(f'Invalid return strategy - {return_strategy}')
        else:
            items.append(main_obj)
        return items

    # if else check that whether it is an xpath or jpath or regex
    def exec_codes(self, response, ext_codes={}):
        ext_codes = ext_codes or self.ext_codes
        selector_values = defaultdict(list)
        selector_name = response.meta.get('selector') or self.default_selector
        codes = {c: v for c, v in ext_codes.items() if v.get("selector", self.default_selector) == selector_name}
        main_obj, selectors = self.iterate_exec_codes(selector_name, response, codes)
        for selector_name, blocks in selectors.items():
            objs = []
            codes = {c: v for c, v in ext_codes.items() if v.get("selector") == selector_name}
            for block in blocks:
                obj, _ = self.iterate_exec_codes(selector_name, block, codes)
                objs.append(obj)
            selector_values[selector_name] = objs

        items = self.get_mix_items(main_obj, selectors, selector_values, ext_codes)
        return items

    def apply_cleanup_func(self, clean_ups, key, obj):
        for clean_up in clean_ups:
            if not obj[key]:
                break
            obj[key] = eval(clean_up)
        return obj[key]

    def apply_xpath(self, selector, paths, return_type=Statics.RETURN_TYPE_DEFAULT):
        values = []
        for path in paths:
            value = selector.xpath(path)
            if return_type != Statics.RETURN_TYPE_SELECTOR:
                value = value.extract()
            values.extend(value)
        return values

    def apply_jpath(self, selector, paths):
        if isinstance(selector, str):
            selector = json.loads(selector)
        elif isinstance(selector, TextResponse):
            selector = json.loads(selector.text)
        value = []
        for path in paths:
            jsonpath_expr = parse(path)
            value.extend([match.value for match in jsonpath_expr.find(selector)])
        return value

    def apply_regex(self, selector, paths):
        if isinstance(selector, str):
            selector = json.loads(selector)
        elif isinstance(selector, TextResponse):
            selector = selector.text
        value = []
        for path in paths:
            value.extend(re.findall(path, selector, re.S))
        return value

    def return_value(self, value, return_type):
        if not value:
            return value
        if return_type == Statics.RETURN_TYPE_INT:
            return int(value[0])
        if return_type == Statics.RETURN_TYPE_STRING:
            return value[0]
        elif return_type in [Statics.RETURN_TYPE_LIST, Statics.RETURN_TYPE_SELECTOR]:
            return [v for v in value if v]
        elif return_type == Statics.RETURN_TYPE_JOIN:
            return ' '.join(value)
        elif return_type in [Statics.RETURN_TYPE_JSON]:
            return json.loads(value[0])
        elif return_type in [Statics.RETURN_TYPE_SELECTOR_JSON]:
            return [json.loads(v) for v in value]
        else:
            self.logger.error(f'Unknown return type - {return_type}')

    # dict to item_class depending on whether its an product item or index item
    def generate_item(self, obj, item_class):
        item = item_class()
        temp_fields = dict()
        item['temp_fields'] = temp_fields
        for key, value in obj.items():
            if key in item_class.fields:
                item[key] = obj.get(key)
            elif key not in self.ignore_fields:
                temp_fields[key] = value
        return item

    def _get_ordered_ext_keys(self, ext_codes):
        keys = ext_codes.keys()
        ordered_keys = []
        for key in keys:
            if key.startswith(Statics.TEMP_FIELD_PREFIX):
                ordered_keys.append(key)
        for key in keys:
            if key not in ordered_keys:
                ordered_keys.append(key)
        return ordered_keys

    def url_joins(self, response, obj, keys):
        for key in keys:
            val = obj.get(key)
            if val:
                if isinstance(val, list):
                    obj[key] = [response.urljoin(v) for v in val]
                else:
                    obj[key] = response.urljoin(val)
        return obj
