# static class for generic methods
import re
import hashlib
import os
import csv
import codecs
from io import BytesIO
from datetime import datetime
from unidecode import unidecode
from w3lib.html import replace_entities, remove_tags


class Utility:

    @staticmethod
    def sanitize(text):
        if text:
            text = unidecode(text)
            text = replace_entities(text)
            text = remove_tags(text)
            text = re.sub('\\s+', ' ', text)
            text = text.strip()
        return text

    @staticmethod
    def format_number(text, return_type):
        text = str(text) if text else text
        if Utility.is_empty(text):
            return None
        text = text.replace(',', '.')
        try:
            text = Utility.remove_html_from_text(text)
            float_text = re.search(r'([\d\.]+)', text, re.S).group(1).strip()
            val = return_type(float_text)
        except:
            val = None
            print("ERROR IN FORMATTING PRICE INFORMATION")
        return val

    @staticmethod
    def is_not_empty(param):
        if isinstance(param, str):
            param = param.strip()
        if param:
            return True
        else:
            return False

    @staticmethod
    def is_empty(param):
        if isinstance(param, str):
            param = param.strip()
        if param:
            return False
        else:
            return True

    @staticmethod
    def get_fingerprint(url):
        if not url:
            return None
        return hashlib.sha224(url.encode('utf-8')).hexdigest()

    @staticmethod
    def change_datetime_format(date_string, from_fmt="%Y-%m-%d", to_fmt="%Y-%m-%d"):
        return datetime.strptime(date_string, from_fmt).strftime(to_fmt)

    @staticmethod
    def read_csv_from_response(response):
        try:
            buffer = BytesIO(response.body)
        except:
            buffer = BytesIO(response.content)
        decoder = codecs.getreader('utf-8')
        return list(csv.DictReader(decoder(buffer, errors='strict')))

    @staticmethod
    def read_csv(fp, encoding="utf-8", delimiter=","):
        with open(fp, encoding=encoding) as f:
            csvreader = csv.DictReader(f, delimiter=delimiter)
            for line in csvreader:
                yield line

    @staticmethod
    def write_csv(fp, data, fieldnames=[], encoding="utf-8", delimiter=","):
        if not data:
            return
        if not fieldnames:
            fieldnames = list(data[0].keys())
        with open(fp, "w", encoding=encoding, newline='') as w:
            csvwriter = csv.DictWriter(w, delimiter=delimiter, fieldnames=fieldnames)
            csvwriter.writeheader()
            for line in data:
                line = {k: v.replace('\n', ' ') if v else v for k, v in line.items()}
                csvwriter.writerow(line)

    @staticmethod
    def get_config_name(website):
        config = website.replace("https:", '').replace('http:', '').strip(' /')
        config = config.replace("www.", '').replace(".", "_").replace("-", "_")
        return config

    @staticmethod
    def get_allowed_domains(websites):
        allowed_domains = []
        for website in websites:
            domain = website.replace("https:", '').replace('http:', '').strip(' /').replace("www.", '')
            allowed_domains.append(domain)
        return allowed_domains

    @staticmethod
    def match_rgx(line, regxes):
        if not line:
            return []

        if not isinstance(line, list):
            line = [line]

        results = []
        for l in line:
            for rgx in regxes:
                results.extend(rgx.findall(l))
        return results
