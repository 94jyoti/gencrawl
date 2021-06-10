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
from shutil import which
from gencrawl.middlewares.selenium_request import GenSeleniumRequest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from collections import defaultdict
from scrapy.http import HtmlResponse
from collections.abc import Iterable
from scrapy.selector import Selector
from abc import ABC, abstractmethod
from gencrawl.settings import CONFIG_DIR, RES_DIR
from gencrawl.util.temp_config_setup import TempConfig


class BaseSpider(Spider):

    @classmethod
    def from_crawler(cls, crawler, config, *args, **kwargs):
        assert config
        # temporary config set up from google sheet
        TempConfig().main(CONFIG_DIR)
        config = config.strip(' /').replace("https://", '').replace('http://', '').replace(
            "www.", '').replace(".", "_").replace("-", "_")
        config_filename = config + Statics.CONFIG_EXT
        config_fp = os.path.join(CONFIG_DIR, config_filename)
        config = json.loads(open(config_fp).read())
        custom_settings = config[cls.crawl_type].get("custom_settings") or config.get("custom_settings")
        if custom_settings:
            crawler.settings.frozen = False
            crawler.settings.update(custom_settings)
            crawler.settings.freeze()
        return super().from_crawler(crawler, config, *args, **kwargs)

    def __init__(self, config, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.settings = get_project_settings()
        self.urls = kwargs.get("urls")
        self.input_file = kwargs.get("input_file")
        self.config = config
        self.specific_config = config[self.crawl_type]
        self.input = self._get_start_urls(self.urls, self.input_file)
        self.job_id = uuid.uuid1().hex
        self.allowed_domains = config['allowed_domains']
        self.website = config['website']
        self.parsing_type = self.specific_config.get('parsing_type') or config['parsing_type']
        self.crawl_method = self.specific_config.get("crawl_method") or config['crawl_method']
        self.wait_time = self.specific_config.get("wait_time") or config.get('wait_time')
        self.default_parsing_type = self.specific_config.get("parsing_type") or config.get('parsing_type')
        self.navigation = self.specific_config.get("navigation")
        self.pagination = self.specific_config.get("pagination")
        self.ext_codes = self.specific_config['ext_codes']
        self.retry_condition = self.ext_codes.pop("retry_condition", None)
        self.default_return_type = Statics.RETURN_TYPE_DEFAULT
        self.default_selector = Statics.SELECTOR_DEFAULT
        self.all_url_keys = [Statics.URL_KEY_FINANCIAL_LISTING, Statics.URL_KEY_FINANCIAL_DETAIL]
        self.ignore_meta_fields = Statics.IGNORE_META_FIELDS

    def _get_start_urls(self, urls, input_file):
        objs = list()
        if urls:
            for url in urls.split("|"):
                objs.append({self.url_key: url})
        elif input_file:
            input_file = os.path.join(RES_DIR, input_file)
            for line in open(input_file, encoding="utf-8"):
                if line.startswith("{"):
                    obj = json.loads(line)
                    obj = {k: v for k, v in obj.items() if k not in Statics.IGNORE_INPUT_FIELDS}
                else:
                    url = re.search(r'.*?(http.*)', line)
                    if url:
                        obj = {self.url_key: url.group(1).strip()}
                objs.append(obj)
        else:
            urls = self.specific_config.get("start_urls", [])
            for url in urls:
                objs.append({self.url_key: url})

        if not objs:
            self.logger.error("Input not provided.")
        self.logger.info("Total urls to be crawled - {}".format(len(objs)))
        return objs

    def make_request(self, url, callback=None, method=Statics.CRAWL_METHOD_DEFAULT, headers=None, meta=None, body=None,
                     wait_time=Statics.WAIT_TIME_DEFAULT, wait_until=None, iframe=None, dont_filter=False):
        headers = headers or dict()
        meta = meta or dict()
        if method == Statics.CRAWL_METHOD_SELENIUM:
            request = GenSeleniumRequest(url=url, callback=callback, meta=meta, wait_time=wait_time,
                                         wait_until=wait_until, iframe=iframe, dont_filter=dont_filter)
        else:
            if method == Statics.CRAWL_METHOD_GET:
                request = Request(url, callback=callback, meta=meta, headers=headers, dont_filter=dont_filter)
            elif method == Statics.CRAWL_METHOD_POST:
                request = Request(url, callback=callback, method="POST", meta=meta, headers=headers, body=body,
                                  dont_filter=dont_filter)
            else:
                self.logger.error(f"Request type is not supported - {method}")
        return request

    def start_requests(self):
        for obj in self.input:
            url = obj[self.url_key]
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

    def get_pagination_urls(self, response, ext_codes=None):
        if not self.pagination:
            return
        pagination_ext_codes = ext_codes or {"pagination": self.pagination}
        pagination_urls = self.exec_codes(response, pagination_ext_codes)[0].get("pagination")
        pagination_urls = [response.urljoin(url) for url in pagination_urls]
        return pagination_urls

    def get_pagination_requests(self, pagination_urls, pagination_fields):
        if not pagination_urls:
            return
        if isinstance(pagination_urls, str):
            pagination_urls = [pagination_urls]
        for url in pagination_urls:
            meta = pagination_fields
            meta[self.url_key] = url
            meta['selector'] = Statics.SELECTOR_ROOT
            yield self.make_request(url, callback=self.parse, meta=meta)

    def parse(self, response):
        pagination_fields = response.meta
        pagination_fields = {k: v for k, v in pagination_fields.items() if k not in Statics.IGNORE_META_FIELDS}
        default_item = self.get_default_item(response)
        items_or_req = self.get_items_or_req(response, default_item=default_item)
        navigation = self.parse_navigation(response, items_or_req)
        if isinstance(navigation, Iterable) and (not isinstance(navigation, dict)):
            yield from navigation
        else:
            yield navigation

        pagination_urls = self.get_pagination_urls(response)
        yield from self.get_pagination_requests(pagination_urls, pagination_fields)

    def parse_navigation(self, response, items):
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
                        items = self.prepare_items(response, default_item=item)[0]
        return items

    def get_meta(self, meta):
        meta = {k: v for k, v in meta.items() if k not in self.ignore_meta_keys}
        return meta

    def iterate_exec_codes(self, selector_name, selector, ext_codes, obj=None):
        obj = obj or dict()
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

    def apply_return_strategy(self, main_obj, selectors, selector_values, ext_codes):
        items = [main_obj]
        if selectors:
            for selector_name in selector_values:
                p_values = list()
                values = main_obj.get(selector_name)
                if values:
                    for value in values:
                        if isinstance(value, Selector):
                            value = value.extract()
                        p_values.append(value)
                    main_obj[selector_name] = p_values

            for selector_name, values in selector_values.items():
                return_strategy = ext_codes[selector_name].get(
                    "child_return_strategy") or Statics.RETURN_STRATEGY_DEFAULT
                if return_strategy == Statics.RETURN_STRATEGY_SINGLE_ITEM:
                    # values getting updated to the main item
                    for item in items:
                        for value in values:
                            item.update(value)
                            break
                elif return_strategy == Statics.RETURN_STRATEGY_SINGLE_OBJECT:
                    key = selector_name.replace(Statics.TEMP_FIELD_PREFIX, "")
                    for item in items:
                        item[key] = values[0] if values else None
                elif return_strategy == Statics.RETURN_STRATEGY_MULTIPLE_OBJECTS:
                    key = selector_name.replace(Statics.TEMP_FIELD_PREFIX, "")
                    for item in items:
                        item[key] = values
                elif return_strategy == Statics.RETURN_STRATEGY_MULTIPLE_ITEMS:
                    new_items = []
                    for item in items:
                        for value in values:
                            n_item = deepcopy(item)
                            n_item.update(value)
                            new_items.append(n_item)
                    items = new_items
                else:
                    self.logger.error(f'Invalid return strategy - {return_strategy}')

        return items

    # if else check that whether it is an xpath or jpath or regex
    def exec_codes(self, response, ext_codes=None, default_obj=None):
        default_obj = default_obj or dict()
        ext_codes = ext_codes or self.ext_codes
        selector_values = defaultdict(list)
        # try-except to handle those cases where response object is still not tied to a meta,
        # like calling this function from a middleware
        try:
            selector_name = response.meta.get('selector') or self.default_selector
        except AttributeError as _:
            selector_name = self.default_selector
        codes = {c: v for c, v in ext_codes.items() if v.get("selector", self.default_selector) == selector_name}
        main_obj, selectors = self.iterate_exec_codes(selector_name, response, codes, obj=default_obj)
        for selector_name, blocks in selectors.items():
            objs = []
            codes = {c: v for c, v in ext_codes.items() if v.get("selector") == selector_name}
            for block in blocks:
                obj, _ = self.iterate_exec_codes(selector_name, block, codes)
                objs.append(obj)

            selector_values[selector_name] = objs
        items = self.apply_return_strategy(main_obj, selectors, selector_values, ext_codes)
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
            for val in value:
                if val:
                    return val
        elif return_type in [Statics.RETURN_TYPE_LIST, Statics.RETURN_TYPE_SELECTOR]:
            return [v for v in value if v]
        elif return_type == Statics.RETURN_TYPE_JOIN:
            return ' '.join(value)
        elif return_type in [Statics.RETURN_TYPE_JSON]:
            if isinstance(value[0], str):
                value = json.loads(value[0])
            else:
                value = value[0]
            return value
        elif return_type in [Statics.RETURN_TYPE_SELECTOR_JSON]:
            values = []
            for v in value:
                if isinstance(v, str):
                    values.append(json.loads(v))
                else:
                    values.append(v)
            return values
        else:
            self.logger.error(f'Unknown return type - {return_type}')

    # prepare item dict from ext_codes from the config of website
    @abstractmethod
    def prepare_items(self, response, default_item=None):
        pass

    # callback to be called from parse method. It should return a list of
    # items or requests or a combination of both
    @abstractmethod
    def get_items_or_req(self, response, default_item=None):
        pass

    # item dict to item_class depending on whether its an product item or listing item or any other type
    # fields that are not defined in item class will be moved to temp_fields
    def generate_item(self, obj, item_class):
        item = item_class()
        temp_fields = dict()
        item['temp_fields'] = temp_fields
        for key, value in obj.items():
            if key in item_class.fields:
                item[key] = obj.get(key)
            elif key not in self.ignore_meta_fields:
                temp_fields[key] = str(value)[:Statics.MAX_OTHER_FIELDS_LENGTH] + "..."
        return item

    # return field names from the ext_codes. The temp_ fields are assigned first in the queue and
    # hence executed first
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

