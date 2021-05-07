# static class for generic methods
import re
import hashlib
import os
from datetime import datetime


class Utility:

    @staticmethod
    def remove_html_from_text(text):
        result = None
        if Utility.is_not_empty(text):
            text = text.replace('&amp;', '&').replace('<br>', '').replace('\n', ' ').replace('\t', ' ')
            text = re.sub(r'<[^>]*>', " ", text)
            result = re.sub(r'\s+', " ", text).strip()
        return result

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



