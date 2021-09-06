from gencrawl.items.hospital.hospital_detail_item import HospitalDetailItem
from gencrawl.util.utility import Utility
from gencrawl.util.statics import Statics
import csv
import os
from gencrawl.settings import RES_DIR


class DHCPipeline:

    def open_spider(self, spider):
        self.redundant_fields = ['temp_fields']
        self.decision_tags = spider.config.get("decision_tags") or {}

    def parse_field(self, field):
        if isinstance(field, bool):
            field = "true" if field else "false"
        elif isinstance(field, int) or isinstance(field, float):
            field = str(field)
        return Utility.sanitize(field)

    def parse_item(self, item):
        parsed_item = dict()
        for key in item.keys():
            value = item[key]
            if isinstance(value, str):
                parsed_item[key] = self.parse_field(value)
            elif key not in self.redundant_fields:
                parsed_item[key] = value
        return parsed_item

    def split_name(self, item):
        raw_name = item.get("raw_full_name")
        if raw_name:
            raw_name = raw_name.split(" ")
            if not item.get("first_name") and len(raw_name) > 0:
                item['first_name'] = raw_name[0].strip()
            if not item.get("last_name") and len(raw_name) > 1:
                item['last_name'] = raw_name[-1].strip()
            if not item.get("middle_name") and len(raw_name) == 3:
                item['middle_name'] = raw_name[1]
        return item

    def process_item(self, item, spider):
        if isinstance(item, HospitalDetailItem):
            item = self.parse_item(item)
            if not self.decision_tags.get("dont_split_name"):
                item = self.split_name(item)
        return item
