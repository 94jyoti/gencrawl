from gencrawl.items.hospital.hospital_detail_item import HospitalDetailItem
from gencrawl.util.utility import Utility
from gencrawl.util.statics import Statics
import csv
import os
import re
from gencrawl.settings import RES_DIR


class DHCPipeline:

    def __init__(self):
        self.redundant_fields = ['temp_fields']
        self.pincode_rgx = re.compile(r'([\d]{5})')
        self.state_rgx = re.compile(r'\s([A-Z]{2})\s')
        us_states = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware',
                     'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky',
                     'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi',
                     'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico',
                     'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania',
                     'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont',
                     'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming', 'District of Columbia']
        self.us_states = sorted(us_states, key=len, reverse=True)

    def open_spider(self, spider):
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

    def parse_phone(self, item):
        if item.get("phone"):
            item['phone'] = item['phone'].replace("tel:", "")
        return item

    def parse_address(self, item):
        if not item.get("address"):
            address_keys = ['address_line_1', 'city', 'state', 'zip']
            address_values = [item[k] for k in address_keys if item.get(k)]
            item['address'] = ' '.join(address_values)

        if item.get('address'):
            address = item['address']
            if not item.get('zip'):
                pincode = self.pincode_rgx.search(address, re.S)
                if pincode:
                    item['zip'] = pincode.group(1)

            if not item.get("state"):
                for state in self.us_states:
                    if state.lower() in address.lower():
                        item['state'] = state
                        break

            if item.get("state"):
                state = self.state_rgx.search(address.replace(",", ' ').replace(
                    ';', ' ').replace('\n', ' ').replace('\t', ' '), re.S)
                if state:
                    item['state'] = state.group(1)

        return item

    def process_item(self, item, spider):
        if isinstance(item, HospitalDetailItem):
            item = self.parse_item(item)
            if not self.decision_tags.get("dont_split_name"):
                item = self.split_name(item)
            item = self.parse_phone(item)
            item = self.parse_address(item)
        return item
