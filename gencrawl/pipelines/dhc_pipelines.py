from gencrawl.items.hospital.hospital_detail_item import HospitalDetailItem
from gencrawl.util.utility import Utility
from gencrawl.util.statics import Statics
import requests
import csv
import os
import re
from gencrawl.settings import RES_DIR


class DHCPipeline:

    def __init__(self):
        self.redundant_fields = ['temp_fields']
        self.name_separators = [";", ","]
        self.pincode_rgx = re.compile(r'([\d]{5})')
        self.state_rgx = re.compile(r'\s([A-Z]{2})\s')
        phone_rgx = ['(\(\d{3}\)[-\s]\d{3}[-\s]\d{4})', '(\d{3}[-\s]\d{3}[\s-]\d{4})']
        self.phone_rgx = [re.compile(r) for r in phone_rgx]
        resp = requests.get(Statics.CITY_STATE_GOOGLE_LINK)
        us_cities = set()
        us_states = set()
        suffixes = set()
        designations = set()
        for row in Utility.read_csv_from_response(resp):
            city, state, suffix, designation = row['City'], row['State'], row['Suffix'], row['Designation']
            if city:
                us_cities.add(city.strip())
            if state:
                us_states.add(state.strip())
            if suffix:
                suffixes.add(suffix.strip())
            if designation:
                designations.add(designation.strip())

        self.us_cities = sorted(us_cities, key=len, reverse=True)
        self.us_states = sorted(us_states, key=len, reverse=True)
        self.suffixes = sorted(suffixes, key=len, reverse=True)
        self.designations = sorted(designations, key=len, reverse=True)
        self.designations_map = {k: 1 for k in self.designations}
        self.suffixes_map = {k: 1 for k in self.suffixes}

    def open_spider(self, spider):
        self.decision_tags = spider.config.get("decision_tags") or {}

    def parse_field(self, field):
        if isinstance(field, bool):
            field = "true" if field else "false"
            return  field
        elif isinstance(field, dict):
            return field
        elif isinstance(field, int) or isinstance(field, float):
            return str(field)
        return Utility.sanitize(field)

    def parse_item(self, item):
        parsed_item = dict()
        for key in item.keys():
            value = item[key]
            if isinstance(value, str):
                parsed_item[key] = self.parse_field(value)
            elif isinstance(value, list):
                value = [self.parse_field(v) for v in value]
                parsed_item[key] = value
            elif key not in self.redundant_fields:
                parsed_item[key] = value
        return parsed_item

    def parse_suffix(self, item):
        raw_name = item['raw_full_name']
        for sep in self.name_separators:
            raw_name = raw_name.replace(sep, ' ')
        raw_name = [r.strip() for r in raw_name.split() if r.strip()]
        for part in raw_name:
            if part in self.suffixes_map:
                item['suffix'] = part
                break
        return item

    def parse_designation(self, item):
        def parse_d(name):
            for sep in self.name_separators:
                name = name.replace(sep, ' ')
            name = [r.strip() for r in name.split() if r.strip()]
            d = []
            for part in name:
                if part in self.designations_map:
                    d.append(part)
            return d

        raw_name = item['raw_full_name']
        # parse the designations after first comma
        designation = parse_d(raw_name.split(",", 1)[-1])

        # if not found after first comma, parse from full name
        if not designation:
            designation = parse_d(raw_name)

        if designation:
            item['designation'] = designation

        return item

    def parse_name(self, item):
        raw_name = item.get('raw_full_name')
        designations = item.get('designation') or []
        suffix = item['suffix'] or ''
        for sep in self.name_separators:
            raw_name = raw_name.replace(sep, ' ')
        raw_name = [r.strip() for r in raw_name.split() if r.strip()]
        raw_name = [r for r in raw_name if r not in designations and r != suffix]
        if not item.get("first_name") and len(raw_name) > 0:
            item['first_name'] = raw_name[0].strip()
        if not item.get("last_name") and len(raw_name) > 1:
            item['last_name'] = raw_name[-1].strip()
        if not item.get("middle_name") and len(raw_name) == 3:
            item['middle_name'] = raw_name[1]
        return item

    def parse_fields_from_name(self, item):
        raw_name = item.get("raw_full_name")
        if raw_name:
            if not item.get('suffix'):
                item = self.parse_suffix(item)
            if not item.get("designation"):
                item = self.parse_designation(item)
            item = self.parse_name(item)
        if isinstance(item['designation'], list):
            item['designation'] = '___'.join(item['designation'])
        return item

    def parse_phone(self, item):
        if item.get("phone"):
            item['phone'] = item['phone'].replace("tel:", "")
            for rgx in self.phone_rgx:
                phone = rgx.search(item['phone'], re.S)
                if phone:
                    item['phone'] = phone.group(1)
                    break
        return item

    def parse_fields_from_address(self, item):
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

            if not item.get("city"):
                for city in self.us_cities:
                    if city.lower() in address.lower():
                        item['city'] = city
                        break

            if not item.get("state"):
                for state in self.us_states:
                    if state.lower() in address.lower():
                        item['state'] = state
                        break

            if not item.get("state"):
                state = self.state_rgx.search(address.replace(",", ' ').replace(
                    ';', ' ').replace('\n', ' ').replace('\t', ' '), re.S)
                if state:
                    item['state'] = state.group(1)

            if not item.get("phone"):
                for rgx in self.phone_rgx:
                    phone = rgx.search(address, re.S)
                    if phone:
                        item['phone'] = phone.group(1)
                        break

            if item.get("city") and not item.get("address_line_1"):
                address_lines = item['address'].split(item['city'])[0].strip().split(",", 1)
                item['address_line_1'] = address_lines[0]
                if len(address_lines) == 2:
                    item['address_line_2'] = address_lines[1]

        return item

    def process_item(self, item, spider):
        if isinstance(item, HospitalDetailItem):
            item = self.parse_fields_from_name(item)
            item = self.parse_phone(item)
            item = self.parse_fields_from_address(item)
            item = self.parse_item(item)
        return item
