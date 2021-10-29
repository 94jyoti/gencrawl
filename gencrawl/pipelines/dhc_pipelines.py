from gencrawl.items.hospital.hospital_detail_item import HospitalDetailItem
from gencrawl.util.utility import Utility
from gencrawl.util.statics import Statics
import requests
import csv
import os
import re
from gencrawl.settings import RES_DIR
from lxml import html
import unidecode


class DHCPipeline:

    def __init__(self):
        self.all_fields = ['npi', 'doctor_url', 'raw_full_name', 'first_name', 'middle_name', 'last_name', 'suffix',
                           'designation', 'speciality', 'affiliation', 'practice_name', 'address_raw', 'address',
                           'address_line_1', 'address_line_2', 'address_line_3', 'city', 'state', 'zip', 'phone', 'fax',
                           'email']
        self.redundant_fields = ['temp_fields']
        self.name_separators = [","]
        # if this rgx is not sufficient, add without \b at end
        pincode_rgx = [r'\b([\d]{5}-[\d]{4})\b', r'\b([\d]{5})\b']
        self.pincode_rgx = [re.compile(r) for r in pincode_rgx]
        self.state_rgx = re.compile(r'\b([A-Z]{2})\b', re.I)

        # formats -
        # (123)-123-1234, (123) 123 1234, 123-123-1234, 123 123 1234
        phone_rgx = [r'(\(\d{3}\)[\.\-\s]\d{3}[\.\-\s]\d{4})', r'(\d{3}[\.\-\s]\d{3}[\.\s\-]\d{4})',
                     r'(\(\d{3}\)\d{3}[\.\-\s]\d{4})']
        self.phone_rgx = [re.compile(r) for r in phone_rgx]
        self.phone_keywords = ["tel", "ph", "telephone", "phone", "p:", "(p)"]
        self.fax_keywords = ["fax", "fx", "f:", "(f)"]

        email_rgx = ['([\w\-\.]+@\w[\w\-]+\.+[\w\-]+)']
        self.email_rgx = [re.compile(r) for r in email_rgx]

        resp = requests.get(Statics.CITY_STATE_GOOGLE_LINK)
        us_cities = set()
        us_states = set()
        suffixes = set()
        designations = set()
        self.practice_tags = set()
        self.address_tags = set()
        self.address_text_to_remove = set()
        self.address1_text_to_remove = set()
        for row in Utility.read_csv_from_response(resp):
            city, state, suffix, designation = row['City'], row['State'], row['Suffix'], row['Designation']
            text_to_remove, text_to_remove1 = row['Text To Remove'], row['Text To Remove From Address1 Start']
            practice_tag = row['Practice Tags']
            address_tag = row['Address Tags']
            if city:
                us_cities.add(city.strip())
            if state:
                us_states.add(state.strip())
            if suffix:
                suffixes.add(suffix.strip())
            if designation:
                designations.add(designation.strip())
            if text_to_remove:
                self.address_text_to_remove.add(text_to_remove.strip())
            if text_to_remove1:
                self.address1_text_to_remove.add(text_to_remove1)
            if practice_tag:
                self.practice_tags.add(practice_tag.strip())
            if address_tag:
                self.address_tags.add(address_tag.strip())

        self.us_cities = sorted(us_cities, key=len, reverse=True)
        self.us_states = sorted(us_states, key=len, reverse=True)
        self.suffixes = sorted(suffixes, key=len, reverse=True)
        self.designations = sorted(designations, key=len, reverse=True)
        self.designations_map = {k: 1 for k in self.designations}
        self.suffixes_map = {k: 1 for k in self.suffixes}

    def open_spider(self, spider):
        self.decision_tags = spider.config.get("decision_tags") or {}
        if self.decision_tags.get("pincode_rgx"):
            for r in self.decision_tags['pincode_rgx']:
                self.pincode_rgx.append(re.compile(r'{}'.format(r)))
        if self.decision_tags.get("phone_rgx"):
            for r in self.decision_tags['phone_rgx']:
                self.phone_rgx.append(re.compile(r'{}'.format(r)))
        if self.decision_tags.get("ignore_cities"):
            for city in self.decision_tags.get("ignore_cities"):
                self.us_cities.remove(city)

    def parse_field(self, field):
        if isinstance(field, bool):
            field = "true" if field else "false"
            return field
        elif isinstance(field, dict):
            return field
        elif isinstance(field, int) or isinstance(field, float):
            return str(field)
        return Utility.sanitize(field)

    def parse_item(self, item):
        parsed_item = dict()
        for key in item.keys():
            value = item[key]
            if key == 'address_raw':
                if value:
                    if isinstance(value, list):
                        value = ' '.join(value)
                    value = re.sub('\\s+', ' ', value)
                parsed_item[key] = value
                continue
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

    def parse_designation_backup(self, item):
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

    # default implementation takes designation after first comma
    def parse_designation(self, item):
        raw_name = item['raw_full_name']
        ignore_designations = []
        for key in ['first_name', 'middle_name', 'last_name']:
            if item.get(key):
                ignore_designations.append(item[key])
        # parse the designations after first comma
        if ',' in raw_name:
            designation = raw_name.split(",", 1)[-1]
            suffix = item.get("suffix") or ''
            designation = designation.replace(suffix, '').strip(", ")
            designation = [d.strip() for d in designation.split(",")]
            item['designation'] = designation
        else:
            item = self.parse_designation_backup(item)
        if item.get("designation"):
            item['designation'] = [d for d in item['designation'] if d not in ignore_designations]
        return item

    def parse_name(self, item):
        raw_name = item.get('raw_full_name')
        if "," in raw_name:
            raw_name = raw_name.split(",")[0]

        raw_name = [r.strip() for r in raw_name.split() if r.strip()]
        designations = item.get('designation') or []
        suffix = item.get('suffix') or ''
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
        return item

    # Receive a line that have an address + city and separate them
    def find_city(self, item, address_raw):
        for index, line in reversed(list(enumerate(address_raw))):
            found = False
            words = line.split()
            for i in range(0, len(words)):
                city = ' '.join(words[i:])
                if city in self.us_cities:
                    found = True
                    if not item.get("city"):
                        item['city'] = city
                    address_raw[index] = address_raw[index].replace(city, '')
            if found:
                break
        address_raw = [a.strip().strip(",").strip() for a in address_raw if a and a.strip()]
        return item, address_raw

    # return parsed item with zip & index in list where zip is found
    def find_zip(self, item, address_raw):
        address_upto_idx = len(address_raw)
        for i, adr in reversed(list(enumerate(address_raw))):
            to_break = False
            for rgx in self.pincode_rgx:
                pincode = rgx.search(adr)
                if pincode:
                    address_upto_idx = i
                    if not item.get("zip"):
                        item['zip'] = pincode.group(1)
                    to_break = True
                    break
            if to_break:
                break
        return item, address_upto_idx

    def find_email(self, item, address_extra):
        match_from = item.get("email") or address_extra
        item['email'] = Utility.match_rgx(match_from, self.email_rgx)
        return item

    def find_phone_and_fax(self, item, address_extra):

        def get_field_type(line):
            for k in self.phone_keywords:
                if k in line.lower():
                    return "phone"

            for k in self.fax_keywords:
                if k in line.lower():
                    return "fax"

        regexes = self.phone_rgx
        phones = []
        faxes = []
        idx_to_remove = set()
        address_extra = address_extra or []
        for index, addr in enumerate(address_extra):
            phone_or_fax = Utility.match_rgx(addr, regexes)
            if phone_or_fax:
                idx_to_remove.add(index)
                # variable to store whether field type i.e. phone or fax
                field_type = get_field_type(addr)

                # if field type not found, check in last line of address
                if not field_type and index > 0:
                    prev_addr = address_extra[index - 1]
                    if not Utility.match_rgx(prev_addr, regexes):
                        field_type = get_field_type(prev_addr)
                        if field_type:
                            idx_to_remove.add(index - 1)
                # by default make field type - phone
                if not field_type:
                    field_type = 'phone'

                if field_type == 'phone':
                    phones.extend(phone_or_fax)
                elif field_type == 'fax':
                    faxes.extend(phone_or_fax)

        phones = item.get("phone") or phones
        faxes = item.get("fax") or faxes
        item['phone'] = Utility.match_rgx(phones, regexes)
        item['fax'] = Utility.match_rgx(faxes, regexes)
        if self.decision_tags.get("phone_at_start"):
            address_extra = [a for i, a in enumerate(address_extra) if i not in idx_to_remove]
            return item, address_extra
        else:
            return item

    def find_state(self, item, address):
        # state should be in last two lines
        for index, addr in reversed(list(enumerate(address))):
            if not item.get("state"):
                addr = addr.replace(",", " ")
                states = self.state_rgx.findall(addr)
                for state in reversed(states):
                    if state in self.us_states:
                        item['state'] = state
                        break
                if item.get("state"):
                    r = r'\b{}\b'.format(state)
                    if item.get("zip"):
                        address[index] = re.sub(r, '', addr)
                    else:
                        address[index] = address[index].split(f" {state}")[0]
                    break

            if not item.get("state"):
                for state in self.us_states:
                    if len(state) == 2:
                        continue
                    if state.lower() in addr.lower():
                        item['state'] = state
                        if item.get("zip"):
                            address[index] = "".join(address[index].rsplit(state, 1))
                            # address[index].replace(state, "")
                        else:
                            address[index] = address[index].split(f" {state}")[0]
                        break
                if item.get("state"):
                    break

        # if zip is not in address
        if not item.get("zip") and item.get("state") and address:
            address = address[:index+1]
        address = [a.strip().strip(",").strip() for a in address if a and a.strip()]
        return item, address

    def check_practice_name(self, text):
        if text.split(" ")[0].isdigit():
            return False
        for tag in self.practice_tags:
            if tag in text.split():
                return True
        for tag in self.address_tags:
            if tag in text:
                return False
        for t in text.split():
            if t.isdigit():
                return True
        return False

    def find_practice_name(self, item, address):
        if not address:
            return item, address

        is_practice_name = False
        if self.decision_tags.get("practice_may_in_address"):
            is_practice_name = self.check_practice_name((address[0]))

        if is_practice_name or self.decision_tags.get("practice_in_address"):
            practice_name = address[0]
            address = address[1:]
            address = [a for a in address if a != practice_name]
            if not item.get("practice_name"):
                item['practice_name'] = practice_name
        else:
            practice_name = item.get("practice_name")
            if practice_name:
                address = [a for a in address if a != practice_name]
        return item, address

    def find_address_lines(self, item, address):
        if not item.get("address_line_1"):
            if len(address) == 1:
                address = address[0].rsplit(",", 2)
            if len(address) == 3:
                item['address_line_1'], item['address_line_2'], item['address_line_3'] = address
            elif len(address) == 2:
                if ',' in address[0]:
                    item['address_line_1'], item['address_line_2'] = address[0].rsplit(",", 1)
                    item['address_line_3'] = address[1]
                elif ',' in address[1]:
                    item['address_line_1'] = address[0]
                    item['address_line_2'], item['address_line_3'] = address[1].rsplit(",", 1)
                else:
                    item['address_line_1'], item['address_line_2'] = address
            elif len(address) == 1:
                item['address_line_1'] = address[0]
        if item.get('address_line_1'):
            for text in self.address1_text_to_remove:
                if item['address_line_1'].startswith(text):
                    item['address_line_1'] = item['address_line_1'].replace(text, "", 1).strip()
        return item

    def parse_fields_from_address(self, item):
        if item.get('address_raw'):
            address_raw = item['address_raw']
            if self.decision_tags.get("address_as_text"):
                address_raw = address_raw.replace("<br>", "\n").split("\n")
            elif not self.decision_tags.get("address_as_list"):
                address_tree = html.fromstring(address_raw)
                address_raw = address_tree.xpath("//text()")
            address_raw = [a.strip().strip(",").strip() for a in address_raw if a and a.strip().strip(",").strip()]

            address_raw = [a for a in address_raw if a not in self.address_text_to_remove]
            address_raw = [unidecode.unidecode(a) for a in address_raw]
            if self.decision_tags.get("split_address_1_by_comma"):
                a1 = address_raw[0]
                address_raw = address_raw[1:]
                for a in reversed(a1.split(",")):
                    address_raw.insert(0, a.strip())

            item['address_raw_1'] = "___".join(address_raw)
            item, address_upto_idx = self.find_zip(item, address_raw)
            pincode = item.get("zip")
            if pincode:
                address_raw[address_upto_idx] = address_raw[address_upto_idx].split(pincode)[0]
            address = address_raw[:address_upto_idx + 1]

            if self.decision_tags.get("phone_at_start"):
                item, address = self.find_phone_and_fax(item, address)
                item = self.find_email(item, address)
            else:
                address_extra = address_raw[address_upto_idx + 1:]
                item = self.find_phone_and_fax(item, address_extra)
                item = self.find_email(item, address_extra)

            item, address = self.find_state(item, address)
            item, address = self.find_city(item, address)
            item, address = self.find_practice_name(item, address)
            item = self.find_address_lines(item, address)
        else:
            item = self.find_phone_and_fax(item, None)
            item = self.find_email(item, None)
        return item

    def combine_address(self, item):
        if not item.get('address'):
            address_keys = ['address_line_1', 'address_line_2', 'address_line_3', "city"]
            address_values = [item[k].strip() for k in address_keys if item.get(k) and item[k].strip()]
            first_part_address = " ".join(address_values)
            address_keys = ['state', 'zip']
            address_values = [item[k].strip() for k in address_keys if item.get(k) and item[k].strip()]
            second_part_address = " ".join(address_values)
            if first_part_address or second_part_address:
                item['address'] = ', '.join([first_part_address, second_part_address]).strip(", ")
        return item

    def parse_list_fields(self, item):
        for key in ["designation", "affiliation", "speciality", "practice_name", "phone", "fax", "email"]:
            values = item.get(key) or []
            if isinstance(values, list):
                item[key] = [v.strip() for v in values if v and v.strip()]
                item[key] = ", ".join(item[key])
        return item

    def replace_none_with_blank_string(self, item):
        for key in self.all_fields:
            item[key] = item.get(key) or ''
        return item

    def process_item(self, item, spider):
        if isinstance(item, HospitalDetailItem):
            item = self.parse_fields_from_name(item)
            item = self.parse_fields_from_address(item)
            item = self.combine_address(item)
            item = self.parse_item(item)
            item = self.parse_list_fields(item)
            item = self.replace_none_with_blank_string(item)
        return item